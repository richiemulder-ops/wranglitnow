#!/usr/bin/env python3
"""Sweep every Claude Code transcript touched on a given day, across ALL project
folders for this vault, and print the user turns grouped by session.

Why this exists: Claude Code stores one folder per working directory. Work done
inside a project subfolder under copilot/projects/ lands in a SEPARATE
project folder from the vault root. A
close-session pass that only reads the vault-root folder silently misses most of
the day. See Team Knowledge/session-logs/2026/09/2026-09-11-*_larry_missed-project-sessions.md

Usage:
    python sweep-today-sessions.py [YYYY-MM-DD]

Defaults to today (local time). Output is grouped, newest-project-last, with the
top-level session transcripts only (subagent transcripts are summarised by count,
not dumped, to keep the sweep readable).
"""

import json
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

PROJECTS = Path.home() / ".claude" / "projects"

# Claude Code mangles a working directory into a folder name by replacing every
# path separator and colon with a dash. Derive this vault's stem from where the
# script actually lives, so the sweep works on any machine without editing.
#   C:\Users\sam\Vault  ->  c--users-sam-vault
_VAULT_ROOT = Path(__file__).resolve().parents[2]
VAULT_STEM = (str(_VAULT_ROOT)
              .replace(":", "-")
              .replace("\\", "-")
              .replace("/", "-")
              .lower()
              .lstrip("-"))


def day_bounds(d: date):
    start = datetime.combine(d, datetime.min.time())
    return start.timestamp(), (start + timedelta(days=1)).timestamp()


def project_label(path: Path) -> str:
    """Turn the mangled folder name into something readable."""
    name = path.name
    marker = "-copilot-projects-"
    if marker in name:
        return name.split(marker, 1)[1].replace("-", " ").strip()
    return "vault root"


def user_turns(jsonl: Path):
    out = []
    with jsonl.open(encoding="utf-8", errors="replace") as fh:
        for line in fh:
            try:
                d = json.loads(line)
            except Exception:
                continue
            if d.get("type") != "user":
                continue
            c = d.get("message", {}).get("content")
            if isinstance(c, list):
                t = " ".join(
                    x.get("text", "")
                    for x in c
                    if isinstance(x, dict) and x.get("type") == "text"
                )
            else:
                t = c or ""
            t = t.strip()
            # Skip tool results, hook noise, and interrupt markers.
            if not t or t.startswith("<") or t.startswith("[Request interrupted"):
                continue
            out.append((d.get("timestamp", "")[11:16], t))
    return out


def main():
    target = (
        date.fromisoformat(sys.argv[1]) if len(sys.argv) > 1 else date.today()
    )
    lo, hi = day_bounds(target)

    if not PROJECTS.is_dir():
        print(f"No projects dir at {PROJECTS}")
        return

    sessions = []  # (mtime, project_label, transcript_path, subagent_count)
    for proj in PROJECTS.iterdir():
        if not proj.is_dir() or VAULT_STEM not in proj.name.lower():
            continue
        for jsonl in proj.glob("*.jsonl"):
            mt = jsonl.stat().st_mtime
            if not (lo <= mt < hi):
                continue
            subdir = jsonl.with_suffix("") / "subagents"
            n_sub = len(list(subdir.glob("*.jsonl"))) if subdir.is_dir() else 0
            sessions.append((mt, project_label(proj), jsonl, n_sub))

    if not sessions:
        print(f"No sessions found for {target}.")
        return

    sessions.sort()
    print(f"# Sessions on {target} — {len(sessions)} transcript(s)\n")
    for mt, label, jsonl, n_sub in sessions:
        turns = user_turns(jsonl)
        stamp = datetime.fromtimestamp(mt).strftime("%H:%M")
        print(f"## [{label}] {jsonl.stem[:8]} — last activity {stamp}"
              f" — {len(turns)} user turn(s), {n_sub} subagent run(s)")
        if not turns:
            print("   (no user turns — likely a resumed/empty shell)")
        for hhmm, text in turns:
            print(f"   {hhmm} | {text[:400]}")
        print()


if __name__ == "__main__":
    main()
