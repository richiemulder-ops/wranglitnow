# Actions - Index

One note per meeting action item. Each file is a single action: what it is, who
owns it, which organisation it belongs to, and which meeting raised it.

A root-level register. Linked from the folder map in the root [[AGENTS]].

## The register populates itself

You do not ask for these. **Penn writes them automatically on every meeting
filing.** When a meeting is filed into `PKM/CRM/Meetings/`, extracting its action
items into this folder is part of that same job - one note per item, before the
filing is considered done.

The procedure is [[WS-007-file-a-meeting-and-extract-actions]], step 5. That
Workstream is the single canonical statement of the extraction rules: which
items become actions, how `owner`, `due` and `done` are set, and how the
`action_id` sequence continues. It is not restated here or anywhere else.

Two consequences worth knowing as a reader of this folder:

- **Actions owned by anyone appear here**, not just yours. The register records
  what was committed in the room, by whoever committed it.
- **A meeting with no action items adds nothing.** That is correct, not a
  missed filing.

## How to view them

Open **`_Actions.base`** in this folder. That is the way to read this folder -
not the file list. It gives four table views:

- **Open Actions** (default) - everything still outstanding, soonest due first.
- **Completed** - everything ticked off.
- **All Actions** - open and done together.
- **By Owner** - open actions, grouped by who owns it.
- **By Organisation** - open actions, grouped by client or counterparty.

The `#` column is the `action_id`. That is the action's number - stable, unique
across this folder, and the way to refer to an action in conversation.

## How to mark an action complete

**Tick the Done checkbox in the table row.** The `done` field is a boolean, and
Obsidian Bases renders it as a checkbox you click directly in the row - you do
not need to open the note at all.

The action disappears from **Open Actions** immediately and appears in
**Completed**. It stays visible in **All Actions** either way. Untick it to
reopen it.

`done` is the only completion field. There is no `status` field.

## How to delete an action

Right-click the row in the table and choose **Delete file**. There is nothing
else to clean up - no list to edit, no index entry to remove. The base reads the
folder directly.

Delete, rather than tick, when the action should never have existed. There is no
`cancelled` state.

## SSOT

The action text lives in the `action` frontmatter field of its own note, and
nowhere else. The source meeting note carries the discussion; the action note
points back to it through the `meeting` wikilink. Do not copy the action text
into the meeting note's body, the journal, or any other file.

## Schema

The frontmatter field list is defined in [[GL-002-frontmatter-conventions]]
under the **Actions** entity. Start every new action note from `_template.md` in
this folder. Required fields: `action` and `done` (always `false` at creation).

## Who writes here

Penn creates action notes when filing a meeting, under
[[WS-007-file-a-meeting-and-extract-actions]]. Silas owns the schema. Larry
checks the backlinks at session close.
