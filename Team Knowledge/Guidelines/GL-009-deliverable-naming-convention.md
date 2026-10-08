# GL-009 - Deliverable Naming Convention

> **This Guideline is a general rule every agent reads on every relevant action.** Every file any specialist writes into `Deliverables/` follows the pattern below. It overrides the kebab-case deliverable line in [[GL-001-file-naming-conventions]] §2 for that folder only. Everywhere else in the vault, GL-001 still governs.

## 1. The pattern

```
YYYYMMDD_[Entity]_[Topic]_[DocType]_vMAJOR.MINOR.ext
```

Example: `20260910_Northwind_Q3_Supply_RawData_v1.0.xlsx`

| Segment | Example | Rule |
|---|---|---|
| `YYYYMMDD` | `20260910` | ISO date, no hyphens. The date the version was produced, not the date the work started. |
| `[Entity]` | `Northwind`, `Wranglit`, `Acme` | The client or counterparty the work is for. `Wranglit` only when the work is genuinely about Wranglit itself. |
| `[Topic]` | `Q3_Supply`, `AASB_S2_Draft` | Short and specific. May contain internal underscores. |
| `[DocType]` | `Report`, `RawData` | From the controlled list in §3. Exactly one token, no underscores inside it. |
| `vMAJOR.MINOR` | `v1.0`, `v2.3` | See §4. |
| `.ext` | `.docx`, `.xlsx`, `.md` | Real file extension. |

Underscore separates segments. There are exactly four underscores at segment boundaries, plus any inside `[Topic]`.

## 2. Casing

- Segments use `PascalCase` or `Title_Case`. Capitalise each word.
- Multi-word segments join with an underscore: `Q3_Supply`, `Organisational_Boundary`.
- Never lowercase-kebab inside this folder. Never spaces. Never hyphens as word separators.
- **Wranglit is always written `Wranglit`** — capital C, lowercase h. See [[GL-003-design-system]] §1.
- ASCII only. No accents, no ampersands, no em dashes, no parentheses.

## 3. DocType controlled list

Pick the closest match. Do not invent a new one without adding it here first.

| DocType | Use for |
|---|---|
| `Report` | Findings, analysis, assessments, reviews, briefs delivered to a reader |
| `Research` | Investigative work, market scans, competitor surveys, hire research |
| `Memo` | Short internal position or note to file |
| `AuditMemo` | Audit-facing evidence or methodology note |
| `Deed` | Executable legal instrument (deeds, plan rules, agreements) |
| `Letter` | Formal correspondence on letterhead |
| `Proposal` | Pitch, RFP response, scope and fee document |
| `Template` | Reusable blank a client or the team fills in |
| `Questionnaire` | Client-facing data-collection form |
| `Checklist` | Step list intended to be worked through and ticked |
| `RawData` | Unprocessed source data as received |
| `CalcSheet` | Working calculation, model, or workbook |
| `Deck` | Slide presentation |
| `Graphic` | Infographic, chart, diagram, image asset |
| `Web` | HTML page or web-destined markup |
| `Script` | Build or processing code that produces another artefact |
| `Notes` | Working notes, source drafts feeding a built artefact |

## 4. Versioning

- Start at `v1.0`.
- **Increment MINOR** for fixes: typos, formatting, a corrected figure, a rebuild with no change of position.
- **Increment MAJOR** for substantive change: new sections, changed recommendation, restructure, or anything a reader must re-read in full.
- Reset MINOR to `0` on a MAJOR bump. `v1.4` → `v2.0`.
- **Never overwrite a shipped version.** If the file has left the vault — emailed, attached, signed — the next change is a new file at a new version. Superseded versions move to `Deliverables/_archive/` on close.
- The version number lives in the filename only. Do not also put it in the document footer unless your own format rules call for it.

## 5. Folders and multi-file deliverables

A deliverable with more than one file gets a folder. The folder carries the same pattern **without** the extension and **without** the version:

```
Deliverables/20260910_Northwind_Q3_Supply_Report/
```

Files inside the folder carry the full pattern including version and extension. Sequence prefixes stay allowed for reading order and go before the date:

```
01_20260910_Northwind_Q3_Supply_Questionnaire_v1.0.docx
02_20260910_Northwind_Q3_Supply_CalcSheet_v1.0.xlsx
```

Build scripts and source markdown that feed a built artefact are ordinary members of the folder and take `Script` and `Notes` DocTypes.

## 6. Side-car metadata (optional)

For data artefacts, a matching `.json` side-car may sit beside the file with the identical stem:

```
20260910_Northwind_Q3_Supply_RawData_v1.0.xlsx
20260910_Northwind_Q3_Supply_RawData_v1.0.json
```

The side-car carries `source`, `units`, `checksum`, and any provenance the artefact itself cannot hold. This is optional and used mainly where a downstream agent or tool must ingest the data without opening the workbook.

## 7. Scope boundary

| Location | Convention |
|---|---|
| `Deliverables/` (including `_archive/`, `_scratch/` and `_working/`) | **This Guideline** |
| `copilot/projects/<Name>/` — project workspaces, where project deliverables are filed | **This Guideline**, see §7-ter |
| `PKM/` — journal, CRM, My Life, Documents, Images | [[GL-001-file-naming-conventions]] |
| `Team Knowledge/` — SOPs, Workstreams, Guidelines, session logs | [[GL-001-file-naming-conventions]] |
| `Team/`, `Team Inbox/`, `Expansions/` | [[GL-001-file-naming-conventions]] |

`README.md`, `INDEX.md`, `_archive/`, `_scratch/` and `.gitkeep` keep their literal names inside `Deliverables/`. They are structure, not deliverables.

### 7-bis. `_scratch/` is cleared, not kept

`Deliverables/_scratch/` holds only work that is still temporary — build helpers, one-off migration scripts, intermediate junk, anything a task needs mid-flight and nothing needs afterwards.

**The rule:** the moment a piece of work stops being temporary, `_scratch/` is emptied of it. Whoever finishes the work clears it — in the same turn, not "later".

That means:

- A script has run and its job is done → delete the script.
- An intermediate file has been folded into a real deliverable → delete the intermediate.
- Work is finished but the artefact still matters → move it out to its properly named home under `Deliverables/`, or to `_archive/` if it is superseded.

Nothing in `_scratch/` is a deliverable, so nothing in `_scratch/` survives the task that created it. If a file has sat there past the end of its task, it is either a naming failure (it belongs elsewhere) or dead weight (delete it).

`.gitkeep` stays so the empty folder survives in git. A leftover in `_scratch/` is a Librarian finding at session close: Larry clears it or names the blocker.

### 7-ter. Project work lives in the project folder

`copilot/projects/<Name>/` is the workspace for a project. When work belongs to a project, the finished deliverable is filed **inside that project's folder**, named per this Guideline. It is not filed into `Deliverables/`.

**The two-way rule:**

| The work | Where it is filed |
|---|---|
| Belongs to a project in `copilot/projects/` | `copilot/projects/<Name>/YYYYMMDD_Entity_Topic/` |
| Belongs to no project | `Deliverables/YYYYMMDD_Entity_Topic/` |

Work with no project stays in `Deliverables/` until one of three things happens: it is archived to `Deliverables/_archive/`, it is moved into a project that later adopts it, or a new project is created for it.

Naming does not change with location. Every artefact in a project folder follows the same `YYYYMMDD_[Entity]_[Topic]_[DocType]_vMAJOR.MINOR.ext` pattern as one in `Deliverables/`. Kebab-case does not apply in either place.

**The path is fixed by the plugin.** The Copilot plugin builds its projects root as `<copilotFolder>/projects` in code. The `projectsFolder` key in the plugin's `data.json` is a legacy setting that is read on load but never used to create a project. Moving the projects elsewhere would make the plugin lose every one of them and recreate the folder on the next New Project. Do not relocate `copilot/projects/`.

**Keeping projects findable.** Because the path is four levels deep and plugin-branded, [[Projects]] at the vault root is the index of every project and links to each one. Whoever creates a project adds its row. Whoever notices a missing row adds it.

What always stays in a project folder, and is never renamed:

| Never move or rename | Filed as a deliverable |
|---|---|
| `project.md` — plugin-owned, holds the project id | Reports, statements, registers, manifests |
| `AGENTS.md` / `CLAUDE.md` — the project's contract | Client-facing instruments and templates |
| `project-brief.md` — the standing brief | Rulebooks, memos, reviews |
| `chat-history/` — session transcripts | Data files that are the engagement record |
| `.gitignore` — the project's exclusions | Anything a client might ever see |

Throwaway render PNGs and one-shot test harnesses used to check a layout once are not deliverables anywhere. They go to `Deliverables/_scratch/` and are cleared per §7-bis.

#### Client data inside a deliverable: `_working/`

Some deliverables carry raw detail that must not enter git — client ledger exports, transaction-level lines, account balances, cost-centre structure, and the scripts that processed them.

That detail goes in a `_working/` subfolder of the deliverable, wherever the deliverable lives. `_working/` is git-ignored, so:

- {{USER_NAME}} sees the files in the file tree and in any synced folder.
- The repo never carries the client's financial detail.
- The durable record — reconciliation, manifest, exceptions register, summary — sits at the top level of the deliverable folder and **is** tracked.

`_working/` is not `_scratch/`. Scratch is cleared when the task ends; `_working/` persists for as long as the deliverable does, because re-deriving a mapped ledger from scratch is not free. It is simply never committed.

## 8. Wikilinks

Link a deliverable by its full stem, no extension:

```
[[20260910_Northwind_Q3_Supply_Report_v1.0]]
```

Where a task's `linked_deliverables` array points at a deliverable, the slug is the folder name for multi-file deliverables and the file stem for single files. See [[GL-004-task-resource-linking]].

## 9. Applies from

2026-09-10 forward for all new deliverables. Deliverables produced before that date were renamed in a one-time backfill on 2026-09-10; anything in `_archive/` predating the backfill sweep keeps its original name and is not worth re-cutting.
