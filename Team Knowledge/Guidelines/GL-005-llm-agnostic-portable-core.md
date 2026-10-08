# GL-005 - LLM-Agnostic Portable Core

> **This Guideline is a general rule every agent reads on every relevant action.** It governs WHERE harness-specific mechanism is allowed to live. SOPs, Workstreams, and every `Team/*/AGENTS.md` contract `[[wikilink]]` here rather than restating the rule.

This is the source of truth for the portable-core boundary. Wranglit must run unchanged on Claude Code today and on Codex, Cursor, or any future agent harness tomorrow. That portability is not an accident of how the scaffold happens to be written; it is a rule the whole team enforces on every file they touch.

## The two layers

Wranglit is split into exactly two layers. Every file belongs to one of them.

### Layer 1 - The Portable Core (host-agnostic, canonical)

The portable core is the scaffold's brain. It is the single source of truth for behavior, and it names no harness.

It is made up of:

- **`PKM/`** - the user's knowledge graph.
- **`Team Knowledge/`** - SOPs, Workstreams, Guidelines, Templates, tasks, session-logs.
- **The CONTENT (body) of every `Team/*/AGENTS.md`** - each specialist's canonical contract.

### Layer 2 - The Per-Harness Adapter (host-specific, derived)

The adapter is the thin translation layer that binds the portable core to one specific harness. It is the ONLY place harness-specific mechanism is allowed to live.

- **`.claude/`** for Claude Code (subagent shims at `.claude/agents/<slug>.md`, slash commands at `.claude/commands/`, settings, hooks).
- **`.codex/`** for Codex (when activated).
- **`.cursor/`** for Cursor (when activated).
- Future harnesses get their own top-level adapter directory.

Adapters are **pointers and translators** over the portable contracts, never replacements for them. A Claude Code shim references `Team/<Name> - <Role>/AGENTS.md`; it does not duplicate it. A slash command is a convenience wrapper over a natural-language trigger already described in the portable core; it is not the only way to reach the capability.

## The rules

### Rule 1 - No harness names in the portable core

No file in the portable core may name a specific harness. No "Claude Code", "Codex", "Cursor", "Gemini CLI", or any other product name appears in `PKM/`, in `Team Knowledge/`, or in the body of any `Team/*/AGENTS.md`.

Where a portable contract needs to refer to the thing running it, use a host-agnostic noun: "the harness", "the host", "the agent runtime", "your assistant". Never the brand.

### Rule 2 - No host-specific tool names in the portable core

The portable core describes capabilities, not the tools a particular harness uses to deliver them. Do not write "use the `Agent` tool", "the `Edit` tool", or any other host-specific tool name into a portable file. Describe the action ("dispatch the specialist", "write the file"); let the adapter map it to whatever the active harness calls that action.

### Rule 3 - No slash command as the sole trigger

Every capability must be reachable by a **natural-language trigger** described in the portable contract. A slash command (or any other host-specific shortcut) is a convenience adapter over that trigger, never the only path to it. If the only way to invoke a capability is a slash command, the capability is not portable - rewrite the contract to state the natural-language trigger first, then let the adapter add the shortcut.

This is why every SOP and Workstream documents its trigger as intent ("when the user asks to hire a specialist", "when the user says close session or implies the session is ending"), not as a literal command string.

### Rule 4 - No hardcoded model

No file in the portable core pins a specific model id, model family, or provider. Model selection is a runtime/adapter concern. A contract may describe the SHAPE of work a role needs (deep research, fast lookup, long-context synthesis); it may not name the model that does it.

## How this is enforced

The `agnosticism-audit` section of `validation-script.sh` is the mechanical gate (Silas owns the script). It scans the portable core and **hard-fails** on Claude-coupling: a harness brand name, a host-specific tool name, a slash command presented as a sole trigger, or a hardcoded model id found anywhere in `PKM/`, `Team Knowledge/`, or the body of a `Team/*/AGENTS.md`. A failing audit blocks the release. The adapter directories (`.claude/`, `.codex/`, `.cursor/`) are exempt by design - that is exactly where the coupling is supposed to live.

Run it from the folder root after any edit that may have leaked a harness reference into the portable core:

```
bash validation-script.sh .
```

Exit 0 means the portable core is clean. A non-zero exit with `agnosticism-audit` failures means a harness reference leaked into a portable file; move it down into the adapter layer and re-run.

## Why this matters (the commercial reason)

This boundary is a core v4 selling point, not a stylistic preference.

Single-harness tools lock the buyer to one vendor's runtime. Wranglit does the opposite: because the brain lives in the portable core and only the binding lives in the adapter, the **same** PKM, the **same** Team Knowledge, and the **same** specialist contracts run on Claude Code, Codex, or Cursor with no rewrite. Switching harnesses, or running two at once, costs the user a new adapter directory and nothing else. The user's knowledge and team are theirs, not the harness vendor's.

Keeping the core clean is therefore everyone's job on every write, not a cleanup pass at release time.

## When in doubt

Ask one question: *"If a new harness shipped tomorrow, would this file have to change?"*

- If yes, it is harness-specific and belongs in an adapter directory.
- If no, it belongs in the portable core and must name no harness.

## Updates to this Guideline

If the boundary changes, update this file. Do not duplicate the rule into SOPs, Workstreams, or contracts. They `[[wikilink]]` here and inherit the change automatically.

## References

- [[GL-001-file-naming-conventions]]
- [[GL-002-frontmatter-conventions]]
- [[WS-004-team-retro-and-self-improvement-loop]]
