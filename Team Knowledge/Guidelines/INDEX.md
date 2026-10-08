# Guidelines - Index

**Guidelines are general rules every agent reads on every relevant action.** Where SOPs are skills (procedures the agent runs) and Workstreams are compositions (multi-agent choreography), Guidelines are the static rules and constraints that hold the whole system together. Naming, frontmatter, design system. SOPs and Workstreams `[[wikilink]]` to Guidelines rather than duplicating the rules.

Filename pattern: `GL-NNN-<title>.md`.

## Active Guidelines

| GL | Title | Description |
|---|---|---|
| GL-001 | [[GL-001-file-naming-conventions]] | Kebab-case rules, ISO date prefix on date-driven files, slug rules, image filename pattern. |
| GL-002 | [[GL-002-frontmatter-conventions]] | YAML frontmatter field schemas for all 8 entity types, typing rules, foreign-key convention. Aligns with [[SOP-002-convert-mypka-to-sqlite]]. |
| GL-003 | [[GL-003-design-system]] | Design-system / visual-identity SSOT — the human-readable contract over the Wranglit brand bundle at `Team Knowledge/Brand/Wranglit/`. Colour, type, spacing, imagery, voice, component inventory. Iris authors; Charta/Pixel/Vera read. *(Designer Pack — preinstalled in v3.0.0)* |
| GL-004 | [[GL-004-task-resource-linking]] | One-way Task → Resource linking rule, seven-array task frontmatter contract, `linked_deliverables` slug format, archive-on-close cascade. Read by [[SOP-create-task]], [[SOP-claim-task]], [[SOP-close-task]]. |
| GL-005 | [[GL-005-llm-agnostic-portable-core]] | The portable-core boundary: harness-agnostic core (`PKM/`, `Team Knowledge/`, the body of every `Team/*/AGENTS.md`) vs the per-harness adapter layer (`.claude/`, future `.codex/`, `.cursor/`). No harness names, host tool names, slash-command-only triggers, or hardcoded models in the core. Enforced by the `agnosticism-audit` in `validation-script.sh`. |  <!-- agnosticism-audit:allow -->
| GL-007 | [[GL-007-brand-application-by-format]] | How [[GL-003-design-system]] lands per output format — HTML/web, HTML slide decks, PowerPoint, Word, markdown, and charts in any format. Ends with a 12-line pre-flight checklist every specialist runs before shipping a client-facing artefact. |
| GL-008 | [[GL-008-plain-language-iso-24495-1]] | Plain-language writing standard for Clara's output, per ISO 24495-1:2023. The four governing principles (relevant, findable, understandable, usable), what the standard is not (it is not a controlled vocabulary like ASD-STE100), the read-back evaluation step, and the precedence order when plain language and precision conflict. Supersedes ASD-STE100 for Clara. |
| GL-009 | [[GL-009-deliverable-naming-convention]] | Naming for everything in `Deliverables/`: `YYYYMMDD_[Entity]_[Topic]_[DocType]_vMAJOR.MINOR.ext`, the DocType controlled list, MAJOR/MINOR versioning rules, multi-file folder pattern, optional JSON side-cars. Overrides [[GL-001-file-naming-conventions]] inside `Deliverables/` only. |

*Reserved:* none. Next free Guideline slot is GL-010.

## When to write a new Guideline

- The rule is static and applies across many files or procedures.
- More than one SOP or Workstream needs to know about it.
- Without it, you would copy-paste the same rule into multiple files.

If you find yourself restating the same rule in two files, stop and write a Guideline. Then `[[wikilink]]` to it from both files.
