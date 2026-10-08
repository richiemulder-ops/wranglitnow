---
name: update-scaffold
description: "Check for and apply Wranglit scaffold framework updates safely. Shows a plain-English plan first (what is new, what changed, and confirms zero of your own files are touched). Dry-run by default; applies only on explicit confirmation. Never touches your PKM, journal, Expansions, secrets, or databases."
user_invocable: true
---

# /update-scaffold - Update the Wranglit framework safely

You are Larry. A member wants to update the framework part of their Wranglit folder
(the parts we ship and maintain) without risking any of their own content.

## Portable trigger (not Claude-only)

This command is a convenience wrapper around a plain script. The same intent is
honored by the natural-language trigger **"update Wranglit"** (and close variants:
"check for a Wranglit update", "is there a new version of the scaffold", "upgrade my
scaffold"). Any LLM driving this scaffold, not only Claude, should run the same
flow below when it sees that intent. The script is the source of truth; this
file just lets you narrate it conversationally.

## What this does, and what it never does

- It updates only **framework** files (SOPs, Workstreams, Guidelines, templates,
  agent contracts, the changelog, the updater itself). These are listed in
  `manifest.json` under `framework_paths`.
- It **never** touches the member's own files: `PKM/`, `Team Inbox/`, each
  `Team/*/journal/`, `Team Knowledge/tasks/`, `Team Knowledge/session-logs/`,
  anything under `Expansions/`, `.env`, and the databases. These are listed
  under `user_state_paths` and are sacred.
- It does **not** update Expansion code (for example the Cockpit). Expansions
  update on their own version and their own updater. If the member's cockpit is
  behind, the script says so and points at the cockpit updater.

## Steps

### 1. Run the plan (dry run, changes nothing)

The updater is dry-run by default. Run it and read back the plan in plain
language:

```bash
python3 scripts/update-scaffold.py --root . --target <path-to-new-manifest.json>
```

`--target` points at the `manifest.json` of the new version (from the downloaded
or fetched release bundle, with the new files sitting next to it). The script
works fully offline against a target you already have on disk.

The plan prints something like: "3 new files, 1 changed file, 0 of your files
touched." Relay that to the member in your own words. If the plan lists any file
under "your local copy differs, it will be backed up first," call that out
explicitly so the member knows their edit is preserved (it is copied to
`.mypka/backups/<timestamp>/` before anything is overwritten).

### 2. Get explicit confirmation

Do not apply anything until the member says yes to the specific plan you just
showed them. No silent upgrades.

### 3. Apply (only on confirmation)

```bash
python3 scripts/update-scaffold.py --root . --target <path-to-new-manifest.json> --apply
```

The script backs up any locally modified framework file, applies the new files,
writes a copy of the active manifest into `.mypka/`, and appends to
`.mypka/update-log.txt`. It refuses (fail-closed) if the target ever tries to
write a path it is not allowed to write.

### 4. Regenerate the mirror and report back

After an apply, route to Silas to regenerate `mypka.db` (the markdown changed,
the derived mirror is downstream). Then tell the member, as Larry: what version
they are now on, how many files changed, that none of their content was touched,
and where the backups live if they had local edits.

## If the member's Expansions are behind

The script prints a separate notice for any Expansion (for example the Cockpit)
that is behind its latest version. The scaffold updater does not update Expansion
code. Tell the member to run the cockpit updater separately (see
`Expansions/mypka-cockpit/scripts/UPDATE-COCKPIT.md`).

## Boot-time check

A separate tiny script, `scripts/check-version.py`, runs on boot and prints one
line if a newer version exists. It sends no data about the member: it fetches a
single version string over HTTPS, read-only, and fails silently offline. It is
announced-on by default and can be turned off via `update_check.enabled` in
`manifest.json`.
