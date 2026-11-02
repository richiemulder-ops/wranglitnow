# Changelog

All notable changes to Wranglit. Versions follow [semantic versioning](https://semver.org/).

## [1.1.0] — 2026-11-03

### Added

- **Jarvis Guide** — an optional guide for building Jarvis, a voice butler over the
  vault: a 3D galaxy of your notes, spoken answers, Outlook calendar and email, and
  hand-offs to Larry's team. Twelve prompts for the Claude desktop app, no terminal.
  `jarvis-setup-guide.html` fills in your own names and folders; `README.md` has the
  same steps as plain markdown.

## [1.0.0] — 2026-10-08

First release.

### Added

- **Twelve specialists** with written contracts in `Team/`, bound as host subagents
  on activation. Larry orchestrates; the other eleven execute.
- **The PKM structure** — My Life (Key Elements, Projects, Goals, Habits, Topics),
  CRM (People, Organizations, Meetings), Journal, Documents, Images.
- **The Actions register** — one note per action item, extracted automatically when
  a meeting is filed.
- **Team Knowledge** — 18 SOPs, 6 Workstreams, 7 Guidelines, 9 entity templates.
- **Wranglitdark**, an Obsidian theme in burnt orange on near-black. Colour, type
  and icons only. Every text pairing measured against WCAG 2.2 AA.
- **The onboarding interview** — eight questions on first activation that fill the
  vault with the user's own people, projects and priorities before the first real
  session.
- **Natural-language triggers** for session logging, external knowledge imports,
  meeting filing and Expansion installs. No commands to memorize.
- **The Expansion mechanism** — `Expansions/` ships empty, with the install
  workstream and its security gate in place for packs added later.

### Notes

- Markdown only. No database, no build step, no network calls the system initiates.
- A SQLite mirror can be generated on demand via `SOP-002` when a vault outgrows
  plain files. Markdown stays canonical; the `.db` is a derived layer.
