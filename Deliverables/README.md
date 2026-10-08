# Deliverables

Where the team puts work that belongs to **no project**.

**First check whether the work belongs to a project.** If it does, it is filed inside that project's folder at `copilot/projects/<Name>/`, not here. See [[Projects]] for the list and [[GL-009-deliverable-naming-convention]] §7-ter for the rule.

Work with no project lands here and stays here until one of three things happens: it is archived to `_archive/`, it is moved into a project that adopts it, or a project is created for it.

Naming is identical in both places. Moving a deliverable into a project does not rename it.

## When to use it

- **Pax** delivers a research report -> `Deliverables/YYYYMMDD_[Entity]_[Topic]_Research_v1.0.md`
- **Nolan** delivers a hire workup -> `Deliverables/YYYYMMDD_Wranglit_[Role]_Research_v1.0.md`
- A new specialist delivers a multi-file project -> `Deliverables/YYYYMMDD_[Entity]_[Topic]_[DocType]/`
- **Larry** collects briefs from multiple specialists for a single initiative -> one folder per initiative, same pattern

## When NOT to use it

- Personal life facts (people, projects, goals, habits) -> `PKM/`
- Daily journal entries -> `PKM/Journal/`
- Reference material the team needs forever (SOPs, Workstreams, Guidelines) -> `Team Knowledge/`

Naming convention: **[[GL-009-deliverable-naming-convention]]** governs everything in this folder — `YYYYMMDD_[Entity]_[Topic]_[DocType]_vMAJOR.MINOR.ext`. GL-001 kebab-case does NOT apply here. `README.md`, `_archive/` and `_scratch/` keep their literal names.

## Lifecycle: active and archived

A deliverable lives in active `Deliverables/` while its owning task is open or in-progress. When the owning task closes (done or cancelled), the deliverable moves to `Deliverables/_archive/<YYYY>/<MM>/<original-folder>/`. The closing task records the archive path in its `## Outcome` section.

This is the **archive-on-close cascade**, enforced by [[SOP-close-task]] and governed by [[GL-004-task-resource-linking]]. The link from task to deliverable is one-way (task -> deliverable, never the reverse) — see GL-004 for why. To find which task owned an archived deliverable, grep the closed task tree for the deliverable's slug, or query `mypka.db.wikilinks` if you maintain the SQLite mirror.

### `_scratch/` is temporary only

`_scratch/` holds work that is still temporary — build helpers, one-off scripts, intermediate files. **When a piece of work stops being temporary, clear it out of `_scratch/` in the same turn:** delete a script whose job is done, delete an intermediate that has been folded into a real deliverable, or move a still-useful artefact to its properly named home. Only `.gitkeep` is permanent here. See [[GL-009-deliverable-naming-convention]] §7-bis.

### Orphan deliverables

A deliverable created without a task wrapping it (e.g., a research brief dropped here directly as shared input) is **never owned** by a task and therefore **never archived** by a close. It sits in active `Deliverables/` indefinitely. This is correct behavior; the deliverable is shared input.

### Shared deliverables

A deliverable referenced by multiple tasks (in `linked_deliverables`) is **not archived** when the first of those tasks closes. The sharing check in [[SOP-close-task]] pre-flight catches this. The deliverable archives only when the last referencing task closes.
