# Wranglit Expansions — Installed

Nothing is installed yet. This folder is where feature packs live.

An Expansion is a self-contained add-on — a set of new specialists, a set of new
SOPs, or a local runtime tool. It arrives as a folder with an `expansion.yaml`
manifest, and it is installed by running [[WS-003-install-an-expansion]], never by
copying files in by hand.

| Name | Type | Version | What it does | Source | Installed |
|---|---|---|---|---|---|
| _none_ | | | | | |

## How to install one

1. Drop the Expansion folder into `Expansions/`.
2. Say "install the [name] Expansion" — or just mention that a new folder appeared.
3. Larry runs [[WS-003-install-an-expansion]]: Vex security-reviews it, Nolan merges
   any new specialists into the team, Mack wires any connectors, Silas checks
   integrity, and this index is rebuilt.

Larry scans this folder at session start and announces anything new. He never
auto-installs, and he never auto-launches a runtime Expansion — you start those
yourself.

## Writing your own

See `Expansions/docs/expansion-spec.md` for the manifest format.

---

> Larry rebuilds this file on every session boot from the contents of this folder.
> Install procedure: [[WS-003-install-an-expansion]].
