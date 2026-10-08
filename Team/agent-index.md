# Team - Agent Index

Routing table for the twelve specialists on the team. Six are the core orchestration and knowledge roles; six cover application development (Felix, Vex, Vera) and design (Iris, Charta, Pixel). Larry reads this on every request to decide who handles what. To add a thirteenth, see [[SOP-001-how-to-add-a-new-specialist]].

| Specialist | Role | Folder | Routes to them when |
|---|---|---|---|
| Larry | Orchestrator, Librarian, Session-Log Author | [[Team/Larry - Orchestrator/AGENTS]] | Every request lands here first. Larry never executes domain work; he routes, then synthesizes. |
| Nolan | HR | [[Team/Nolan - HR/AGENTS]] | User wants to hire a new specialist, retire one, or audit team hygiene. Default owner of [[SOP-001-how-to-add-a-new-specialist]]. |
| Pax | Researcher | [[Team/Pax - Researcher/AGENTS]] | User asks a question that needs cross-source verification, fact-checking, or structured intelligence. |
| Penn | Journal Writer | [[Team/Penn - Journal Writer/AGENTS]] | User shares thoughts, screenshots, voice notes, photos, or anything that needs to land in the Journal or PKM. See [[WS-001-daily-journaling]]. |
| Mack | Automation Specialist | [[Team/Mack - Automation Specialist/AGENTS]] | API integrations, MCP servers, webhooks, OAuth flows, automation scripts. Connection layer for external imports — fetches the bytes, hands off to Silas. Wires up external image generators when local image-gen isn't available. |
| Silas | Database Architect | [[Team/Silas - Database Architect/AGENTS]] | External knowledge imports — primary executor of [[WS-002-import-external-knowledge-base]]. Default owner of [[SOP-002-convert-mypka-to-sqlite]]. Frontmatter integrity audits, schema drift, GL-002 compliance. |
| Felix | Frontend Developer | [[Team/Felix - Frontend Developer/AGENTS]] | Build a UI component/page/layout, fix a UI bug, tighten an interaction, refactor onto the design system. Default owner of [[SOP-003-felix-build-a-component]]. |
| Vex | Security Engineer | [[Team/Vex - Security Engineer/AGENTS]] | Security audit, auth/authorization review, credential hygiene, GDPR technical controls, the "safe to ship" gate. Default owner of [[SOP-004-vex-security-audit]]. Runs the WS-003 Expansion security review. |
| Vera | QA Specialist | [[Team/Vera - QA Specialist/AGENTS]] | Visual/UI QA sign-off, WCAG 2.2 AA accessibility, responsive verification, design-system enforcement. Default owner of [[SOP-005-vera-quality-gate]]. |
| Iris | Design System Architect | [[Team/Iris - Design System Architect/AGENTS]] | Author or extend the design system / brand SSOT. Owns [[GL-003-design-system]]; default owner of [[SOP-006-author-a-design-system]] and [[SOP-007-audit-content-for-design-system-compliance]]. |
| Charta | Infographic Designer | [[Team/Charta - Infographic Designer/AGENTS]] | Build an infographic, slide, diagram, or structured visual deliverable (HTML/CSS layout). Default owner of [[SOP-008-build-an-infographic]]. |
| Pixel | Visual Specialist | [[Team/Pixel - Visual Specialist/AGENTS]] | Generate or stylize an image; routes the connection half to Mack when local image-gen is unavailable. Default owner of [[SOP-009-generate-a-styled-image]]. |

## Bootstrap rule

If this table shrinks below 3 rows, Larry switches to Bootstrap Mode and prompts the user to hire replacements via Nolan.

## Adding a new specialist

Follow [[SOP-001-how-to-add-a-new-specialist]]. Nolan owns this procedure.
