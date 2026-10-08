# /close-session

Close **the whole day** across every chat session in every project, write one
session log per project, and write (or rewrite) the day's journal entry.

**Trigger phrases (case-insensitive):** "close session", "close this session",
"close the day", "wrap", "wrap up", "log this session", "log today", "end
session", "we're done for today", "let's stop here" — or when Larry detects the
day is ending.

Run this **once per day**, at the end of the day. It is not per-chat.

---

## Step 0 — SWEEP ALL PROJECTS FIRST (mandatory, never skip)

Claude Code stores **one transcript folder per working directory.** Work done
inside a project subfolder under `copilot/projects/` lands in a **different**
folder from the vault root. Reading only the current session, or only the vault-root folder, misses
most of the day.

Run the sweep script before anything else:

```bash
python "Team Knowledge/scripts/sweep-today-sessions.py"          # today
python "Team Knowledge/scripts/sweep-today-sessions.py" 2026-09-11  # a past day
```

It prints every transcript touched that day, grouped by project, with each user
turn. Read the whole output before writing a single file.

**Timestamp gotcha:** the per-turn times in the transcripts are **UTC**. AEST is
UTC+10, so a 22:34 turn is 08:34 the next morning local. The session header line
(`last activity HH:MM`) is already local. Always report local time to {{USER_NAME}}.

If the sweep returns nothing, say so plainly and stop — do not invent a day.

---

## Step 1 — One session log per project

For each project that had real work, write:

`Team Knowledge/session-logs/YYYY/MM/YYYY-MM-DD-HH-MM_larry_<topic-slug>.md`

- `HH-MM` is that project's last local activity time, so the logs sort in order.
- `<topic-slug>` is a 3–5 word kebab-case summary of that project's work.
- Auto-create the `YYYY/MM/` folder.
- Use the schema in `Team Knowledge/session-logs/_template.md` exactly.
- A session with no real work (an empty shell, a resumed-and-abandoned chat) gets
  folded into another log as a line, not its own file.

Fill every section:

- **Context** — what that project session was about, one or two sentences.
- **What we did** — concrete actions, each naming the specialist who did the work.
- **Decisions made** — Question + Decision. Only things that change how the team
  operates going forward.
- **Insights** — durable, not yet graduated to an SOP/Workstream/Guideline.
- **Realignments** — every correction {{USER_NAME}} made, **verbatim**. These are the
  most valuable lines in the log. Pull them straight from the sweep output.
- **Open threads** — never blank silently. If nothing is open, write that.
- **Next steps** — concrete and short.
- **Cross-links** — the nearest prior session log, plus sibling logs from the
  same day.

## Step 2 — One journal entry for the day

Route to **Penn**: `PKM/Journal/YYYY/MM/YYYY-MM-DD-<slug>.md`.

One entry covering the whole day across all projects, in the house shape (YAML
frontmatter with `date`, `tags`, `links`; then `# DD Month YYYY — <title>`).

- Verify every wikilink target exists before linking. Do not invent entities.
- Cross-link every session log written in Step 1.
- Honest scope only. Do not invent meetings, decisions, or client work.
- **If a journal entry already exists for the day and is now wrong** (for example
  an earlier partial close called it a quiet day), rewrite it. The journal is
  {{USER_NAME}}'s record of the day and must be accurate. Say in chat that it was
  replaced and why.

## Step 3 — Report back

In chat, give {{USER_NAME}}:

- A table of the day: time, project, what happened.
- His corrections from the day, quoted.
- The paths of every file written.
- Any open thread carried into tomorrow.

---

## Frontmatter schema

```yaml
---
agent_id: larry
session_id: <same-slug-as-filename-without-timestamp>
timestamp: <ISO-8601 UTC>
type: close-session
linked_sops: []
linked_workstreams: []
linked_guidelines: []
---
```

## Hard rules

- **Never close from memory.** The sweep in Step 0 is the source of truth, not
  what is in the current context window. Most of the day is not in context.
- Session logs are **append-only** — once written, never edited by the LLM. The
  journal is the exception: it can be rewritten when a partial close got it wrong.
- If an insight reaches "permanent rule" status, propose graduating it to an
  SOP/Guideline/Workstream — don't let it stagnate.
- Over-capture beats under-capture. When in doubt, write the entry.
- This slash command is Claude Code only. The same protocol is honored on other
  hosts via the trigger phrases in `AGENTS.md § Session-Log Triggers`.
