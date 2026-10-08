# WS-007 - File a Meeting and Extract Actions

> **Status: ACTIVE — approved by {{USER_NAME}} 2026-10-06.**
>
> This Workstream canonicalises a flow that ran undocumented for months. Meeting filing into `PKM/CRM/Meetings/` had no Workstream of its own before this file — it lived only in session-logs and in habit. The new half is **step 5**: action extraction into `Actions/` is now part of the same filing job, not a separate request.

- **Owners:** Penn (writes the meeting note and the action notes) + Mack (connection half when the source is a Fireflies/API pull) + Larry (routing and Librarian pass)
- **Triggered by:** "file this meeting", "here's a meeting transcript", "pull my meetings", a Fireflies pull, or a new note appearing in `PKM/CRM/Meetings/` (see root [[AGENTS]] § Meeting-Filing Triggers)
- **Scope:** `PKM/CRM/Meetings/` and `Actions/`
- **References:** [[GL-001-file-naming-conventions]], [[GL-002-frontmatter-conventions]], [[Actions/INDEX]], [[WS-001-daily-journaling]], [[SOP-write-session-log]]

## Purpose

Turn a meeting — a transcript, a Fireflies summary, a set of notes, a voice memo — into two things that stay in sync:

1. One meeting note in `PKM/CRM/Meetings/`, which carries the discussion.
2. One action note per action item in `Actions/`, which carries the commitment.

The second half is the reason this Workstream exists. The Action Register is self-populating: **a meeting is not filed until its actions are filed.** {{USER_NAME}} never has to ask for the actions separately.

## The hard invariant

**The action text lives in exactly one place: the `action` frontmatter field of its own note in `Actions/`.**

The meeting note carries the discussion and the raw `action_items:` list it was filed from. The action note points back at the meeting through the `meeting` wikilink. The action text is never copied into the Journal, a project file, or any other note. This is the SSOT Golden Rule applied to commitments.

## Steps

### 1. Acquire the source — Penn, escalating to Mack

The source arrives one of four ways:

- **{{USER_NAME}} pastes or drops it** — a transcript, a summary, notes, a file in `Team Inbox/`. Penn works directly from it.
- **A Fireflies pull** — Penn escalates the connection half to Mack. Mack fetches, Penn files. Note the UTC date-filter trap: Fireflies filters on UTC, so an AEST morning meeting lands on the previous UTC day. Widen the query window or the call is missed.
- **A voice memo** — transcribe first, then treat as a transcript.
- **{{USER_NAME}} dictates it in chat** — treat as notes.

Record the evidence grade. A verbatim transcript, an AI summary with no transcript, and a human note are three different grades, and the meeting note says which one it is. Nothing is reported as verified that was not verified.

### 2. Write the meeting note — Penn

- **Path:** `PKM/CRM/Meetings/YYYY-MM-DD-<slug>.md`
- **Slug:** per [[GL-001-file-naming-conventions]] — the counterparties and the subject, kebab-case.
- **Frontmatter:** per [[GL-002-frontmatter-conventions]]. `title`, `date`, `org`, `attendees`, `summary`, `action_items`, `topic`, `source`, `status`, `created`, `updated`.
- **Body:** `## Notes` carrying the discussion, plus whatever sectioning the meeting earns. Where the source gave an action list, reproduce it under `## Action Items`.
- **Cross-link** every person, organisation, topic and project per [[WS-001-daily-journaling]] step 4. Stub what does not exist.

### 3. Create or update the CRM entities — Penn

People and organisations named in the meeting get stubs if they do not already have notes. Existing notes are appended to, never overwritten. Same rules as [[WS-001-daily-journaling]] step 4a.

### 4. Record the "Named but not owned" items — Penn

A meeting usually surfaces work that was discussed but never assigned: proposals with no owner, ideas floated, sessions planned with no date. These go in the meeting note body under a `##### Named but not owned on the action list` heading.

**They are not actions.** Step 5 skips this section entirely. Capturing them in the meeting note is what stops them from leaking into the Action Register as phantom commitments.

### 5. Extract the actions into `Actions/` — Penn

This step is mandatory and runs on every meeting filing, with no separate request from {{USER_NAME}}.

#### 5a. Read both sources, body wins

Read **both** the `action_items:` frontmatter array **and** the `## Action Items` body section. They are usually the same list. When they differ — different wording, an item in one and not the other, a different owner — **the body wins**, because the body is where human review lands.

Note the discrepancy in that action note's `## Context`. Do not silently resolve it. The discrepancy is information about the source's reliability.

#### 5b. Scope — what becomes an action

- **Include actions owned by anyone.** Not just {{USER_NAME}}. A commitment made by a client contact, a colleague, or an auditor is an action in the register. The register is a record of what was committed in the room, not a personal to-do list.
- **Exclude everything under "Named but not owned."** No exceptions. If it had no owner on the call, it is not an action.
- **One action per file.** A meeting with eleven action items produces eleven notes. Never pack a list into one note.
- **A meeting with no actions produces no action notes, and that is a correct outcome.** Do not invent an action to avoid an empty result. Do not create a placeholder. Report "no actions" and move on.

#### 5c. Assign the `action_id`

The sequence is continuous across the whole folder and never restarts per meeting.

1. Read the existing filenames in `Actions/`.
2. Take the highest `action_id` present.
3. Carry on from there, one increment per new action.

Numbers are never reused after a delete. If the folder's highest is 64, the next meeting's first action is 65.

#### 5d. Name the file

`NNNN-<slug>.md`, zero-padded to four digits, slug derived from the action itself in kebab-case. `0065-send-the-revised-boundary-document.md`.

The zero-padding is what keeps the folder sorting correctly in a plain file list. The `action_id` in frontmatter is the plain integer — `65`, not `0065`.

#### 5e. Fill the frontmatter

Start from `Actions/_template.md`. The field schema is defined in [[GL-002-frontmatter-conventions]] § Actions and is not restated here. The judgment rules that are specific to extraction:

| Field | Rule |
|---|---|
| `action` | One sentence, the commitment itself. Required. The only required field. |
| `owner` | The CRM `[[wikilink]]` where a CRM person note exists. A plain string where one does not. **Never invent a CRM link** — a link that does not resolve is worse than a plain name. The user themselves is the plain string `{{USER_NAME}}`. |
| `org` | The `[[wikilink]]` to the CRM organisation, inherited from the meeting note's `org`. |
| `meeting` | The `[[wikilink]]` back to the source meeting note. Load-bearing — this is the SSOT backlink. |
| `date_raised` | The meeting date. |
| `due` | **Only when a real date is stated.** "Before the next session", "soon", "end of month", "ASAP" are not dates. Leave it blank. **Never infer a date.** A blank `due` is correct and common. |
| `done` | `false`. Always, on creation. **Penn never judges completion** — not from the transcript, not from a later meeting, not from inference. Only {{USER_NAME}} closes an action. |
| `source_quote` | The transcript timestamp where the action was raised, when the source carries one. Optional. |

#### 5f. Write the `## Context`

One or two lines: why the action exists and what done looks like. The action text itself is **not** repeated here — it lives in the `action` field only.

Where step 5a found a frontmatter/body discrepancy, state it here.

### 6. Report — Penn to Larry

Penn hands back: the meeting note path, the count of action notes created, and the `action_id` range they occupy. Plus any discrepancy found at 5a and any owner that could not be resolved to a CRM note.

### 7. Librarian pass — Larry

At session close, Larry confirms:

- The `meeting` wikilink in each new action note resolves to the meeting note.
- No action text has been duplicated into the meeting note body, the Journal, or a project file.
- The `action_id` sequence has no gaps and no duplicates.
- New CRM stubs are listed in their section's `INDEX.md`.

## What this Workstream does not do

- **Does not close actions.** Status is set by {{USER_NAME}} in the Properties panel. Penn only ever writes `open`.
- **Does not chase actions.** The register is a record, not a reminder system.
- **Does not write a Journal entry for the meeting.** The meeting note is the record. A Journal entry is written only when {{USER_NAME}}'s own reflection on the meeting is also captured, per [[WS-001-daily-journaling]].
- **Does not deduplicate across meetings.** If the same commitment is restated in a later meeting, that is a second action note pointing at a second meeting. The repetition is the signal.

## Naming

All naming questions resolve to [[GL-001-file-naming-conventions]]. All frontmatter schema questions resolve to [[GL-002-frontmatter-conventions]]. Do not restate either here.

## Changelog

- **1.0.0 (2026-10-06)** — Initial. Canonicalises meeting filing into `PKM/CRM/Meetings/`, which had run undocumented, and adds step 5: mandatory action extraction into `Actions/` as part of the same filing job. Extraction rules proven out in the 64-action backfill of the preceding two weeks: both frontmatter and body are read with the body winning on conflict and the discrepancy noted in `## Context`; "Named but not owned" sections never produce actions; actions owned by anyone are included, not just {{USER_NAME}}'s; `due` is set only from a stated date and never inferred; `done: false` always on creation; `owner` uses a CRM wikilink only where the note exists; `meeting` is the SSOT backlink; `action_id` continues the folder-wide sequence with a zero-padded `NNNN-<slug>.md` filename; a meeting with no actions correctly produces no notes.
