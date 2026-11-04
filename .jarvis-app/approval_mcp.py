"""Approval helper for agents run by Jarvis (an MCP server on stdio, standard library only).

Claude Code runs unattended for Larry's jobs and Team chat, so it can't show its own approval
prompt. With --permission-prompt-tool mcp__jarvis__approve, every tool call that would ask the
user (a Bash command on the vault's "ask" list, or one on no list at all) comes here instead.
This asks the Jarvis server, which shows the request in that agent's chat window, and waits for
your Approve or Deny. Rules that deny outright still deny; rules that allow still allow. The
agent's questions (AskUserQuestion) come the same way and go back with your answers.
"""
import json
import os
import sys
import time
import urllib.error
import urllib.request

SERVER = os.environ.get("JARVIS_SERVER", "http://127.0.0.1:4700")
RUN = os.environ.get("JARVIS_RUN", "")        # which job or chat this agent belongs to
TOKEN = os.environ.get("JARVIS_TOKEN", "")    # proves the request comes from that run
WAIT = 30 * 60                                 # give up (deny) after 30 minutes


def call(path, body=None):
    req = urllib.request.Request(SERVER + path, method="POST" if body is not None else "GET",
                                 data=json.dumps(body).encode() if body is not None else None,
                                 headers={"X-Galaxy": "1", "X-Jarvis-Token": TOKEN,
                                          "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read())


def decide(tool_name, tool_input, tool_use_id):
    """Ask Jarvis, then wait for the user's answer."""
    try:
        ticket = call("/api/approval", {"run": RUN, "tool": tool_name, "input": tool_input, "id": tool_use_id})
    except (OSError, ValueError, urllib.error.URLError) as e:
        return {"behavior": "deny", "message": f"Couldn't reach Jarvis to ask for approval ({e})."}
    if ticket.get("decision") == "approve":   # file work inside the vault: allowed without asking
        return {"behavior": "allow", "updatedInput": tool_input}
    if ticket.get("decision") == "deny":      # never allowed (sending email, for one): no need to ask
        return {"behavior": "deny", "message": ticket.get("message") or "Not allowed."}
    deadline = time.time() + WAIT
    while time.time() < deadline:
        time.sleep(1)
        try:
            state = call(f"/api/approval?ticket={ticket['ticket']}")
        except (OSError, ValueError, urllib.error.URLError):
            continue
        if state.get("decision") == "approve":
            return {"behavior": "allow", "updatedInput": tool_input}
        if state.get("decision") == "answer":   # a question: hand the answers back to the agent
            return {"behavior": "allow", "updatedInput": dict(tool_input, answers=state.get("answers") or {})}
        if state.get("decision") == "deny":
            return {"behavior": "deny", "message": state.get("message") or "The user said no. Don't try it another way; carry on without it."}
    return {"behavior": "deny", "message": "No answer from the user in 30 minutes, so this was not approved."}


TOOL = {
    "name": "approve",
    "description": "Ask the user to approve a tool call.",
    "inputSchema": {"type": "object", "properties": {
        "tool_name": {"type": "string"}, "input": {"type": "object"}, "tool_use_id": {"type": "string"}},
        "required": ["tool_name", "input"]},
}


def reply(msg_id, result):
    sys.stdout.write(json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": result}) + "\n")
    sys.stdout.flush()


for line in sys.stdin:
    try:
        msg = json.loads(line)
    except ValueError:
        continue
    method, msg_id = msg.get("method"), msg.get("id")
    if msg_id is None:            # notifications need no answer
        continue
    if method == "initialize":
        reply(msg_id, {"protocolVersion": (msg.get("params") or {}).get("protocolVersion", "2024-11-05"),
                       "capabilities": {"tools": {}}, "serverInfo": {"name": "jarvis", "version": "1.0"}})
    elif method == "tools/list":
        reply(msg_id, {"tools": [TOOL]})
    elif method == "tools/call":
        args = (msg.get("params") or {}).get("arguments") or {}
        if os.environ.get("JARVIS_APPROVE_TEST") == "allow":   # self-test: allow without asking
            decision = {"behavior": "allow", "updatedInput": args.get("input") or {}}
            if args.get("tool_name") == "AskUserQuestion":     # self-test: pick each question's first option
                qs = (args.get("input") or {}).get("questions") or []
                decision["updatedInput"] = dict(args["input"], answers={q["question"]: q["options"][0]["label"] for q in qs})
        else:
            decision = decide(args.get("tool_name", ""), args.get("input") or {}, args.get("tool_use_id", ""))
        reply(msg_id, {"content": [{"type": "text", "text": json.dumps(decision)}]})
    elif method == "ping":
        reply(msg_id, {})
    else:
        sys.stdout.write(json.dumps({"jsonrpc": "2.0", "id": msg_id,
                                     "error": {"code": -32601, "message": "Method not found"}}) + "\n")
        sys.stdout.flush()
