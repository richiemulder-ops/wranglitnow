# Expansions

This folder holds optional add-ons for your Wranglit vault.

Each Expansion is a folder. Drop it in. Larry walks you through the install on the
next session — confirms the manifest, runs the security review, merges any new
agents and SOPs into your team, wires connectors, and validates the result.
Uninstall whenever: Larry runs the symmetric flow and your vault returns to its
prior shape.

Nothing here is required. The scaffold runs without it. Expansions are how the team
grows beyond the twelve specialists that ship with it — new agents, new connectors,
new runtimes.

A list of installed Expansions lives in `INDEX.md`, regenerated each session. The
full install procedure lives in [[WS-003-install-an-expansion]].

---

## Read this before you install one

**An Expansion is code someone else wrote, running on your machine, with access to
your vault.** Treat it the way you would treat any program you did not write
yourself.

Nobody vets, audits or sandboxes the Expansions you choose to install. There is no
store, no review queue, no guarantee. The security review in `WS-003` is Vex reading
the manifest and the code and telling you what he finds — it is a genuine check, but
it is a reading, not a certification.

What this means in practice:

- **Skim the folder before you trust it.** Larry will ask you once per Expansion and
  remember your answer.
- **Look at what it wants access to.** The manifest declares it. The declaration is
  informational — it is not enforced by anything.
- **Be sceptical of anything that wants credentials, network access, or write
  permission outside its own folder.** Those are the three that matter.
- **You are responsible for what you install.** That is not a disclaimer dodge; it
  is just true of any software you add to your own computer.

Writing your own is the safest option. See `docs/expansion-spec.md` for the manifest
format.
