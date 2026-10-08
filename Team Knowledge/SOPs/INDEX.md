# SOPs - Index

**SOPs are agent skills.** Each SOP is a canonical procedure — a step-by-step recipe for one job. They are LLM-agnostic and reusable across agents: an SOP has a **default owner** (the specialist who runs it most often), but any agent can invoke an SOP when they need its procedure. Think of SOPs the way Claude skills work — discrete, named, callable.

Filename pattern: `SOP-NNN-<title>.md`. See [[GL-001-file-naming-conventions]] for slug rules. Numbering follows authorship order, not topic — gaps are intentional and reserve slots for future agents.

## Active SOPs

| SOP | Title | Default owner | Description |
|---|---|---|---|
| SOP-001 | [[SOP-001-how-to-add-a-new-specialist]] | Nolan | Step-by-step procedure to draft and onboard a new team specialist. References [[GL-001-file-naming-conventions]]. |
| SOP-002 | [[SOP-002-convert-mypka-to-sqlite]] | Silas (run by the user via paste-into-LLM prompt) | Generate a SQLite mirror of your Wranglit on demand. Markdown stays canonical; SQLite is a derived performance layer. Body is a paste-into-LLM prompt. |
| SOP-003 | [[SOP-003-felix-build-a-component]] | Felix | Build a UI component end-to-end on the team's design system. *(App Developer Pack — preinstalled in v3.0.0)* |
| SOP-004 | [[SOP-004-vex-security-audit]] | Vex | Run an application-layer security audit / "safe to ship" review. *(App Developer Pack — preinstalled in v3.0.0)* |
| SOP-005 | [[SOP-005-vera-quality-gate]] | Vera | Visual/UI QA quality gate — design-system + WCAG + responsive sign-off. *(App Developer Pack — preinstalled in v3.0.0)* |
| SOP-006 | [[SOP-006-author-a-design-system]] | Iris | Author or extend [[GL-003-design-system]], the brand/visual SSOT. *(Designer Pack — preinstalled in v3.0.0)* |
| SOP-007 | [[SOP-007-audit-content-for-design-system-compliance]] | Iris | Audit a deliverable against GL-003 and report violations. *(Designer Pack — preinstalled in v3.0.0)* |
| SOP-008 | [[SOP-008-build-an-infographic]] | Charta | Build an infographic / structured visual deliverable (HTML/CSS layout). *(Designer Pack — preinstalled in v3.0.0)* |
| SOP-009 | [[SOP-009-generate-a-styled-image]] | Pixel | Generate or stylize an image to the design system; Mack wires the connection half if needed. *(Designer Pack — preinstalled in v3.0.0)* |

*Reserved (genuinely open for future agents):* SOP-010 onward. SOP-003–009 were claimed by the v3.0.0 all-in-one bundle (App Developer Pack → 003–005, Designer Pack → 006–009). Do not back-fill below SOP-010 without coordinating across the team.

## How to add a new SOP

1. Pick the next unused number (`SOP-NNN`) — by authorship order, not topic. Don't reuse reserved numbers.
2. Filename: `SOP-NNN-<kebab-case-title>.md`.
3. Header includes the default owner, status, triggers, references, and an explicit "Reusable by any agent" note — the SOP is a skill, not 1:1 ownership.
4. Reference [[GL-001-file-naming-conventions]] and any other Guideline instead of duplicating its content.
5. Add a row to this index.
