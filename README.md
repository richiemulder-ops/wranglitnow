# Wranglit

A personal knowledge vault that comes with a team.

Wranglit is an Obsidian-compatible folder of plain markdown files, plus twelve AI
specialists who know how to work in it. You open it in Claude Code (or Codex,
Gemini CLI, or Cursor), it interviews you for five minutes, and you have a working
system with your own people, projects and priorities already filed in it.

No database. No app to install. No account. Plain text files on your own machine,
readable in any editor.

---

## What you get

**A structure that holds.** Your life splits into Key Elements, Projects, Goals,
Habits and Topics. People and organizations live in a CRM. Meetings get filed, and
their action items get extracted into a register automatically. Every fact lives in
exactly one file, and everything else links to it.

**Twelve specialists.** Not twelve chatbots — twelve written contracts that tell one
model how to behave in twelve different jobs.

| | |
|---|---|
| **Larry** | Orchestrator. Every request lands here first. He routes, then synthesizes. He never does the work himself. |
| **Penn** | Captures what you say into the journal and the PKM. |
| **Pax** | Researches with cross-source verification. |
| **Nolan** | Hires a thirteenth specialist when you need a role the twelve do not cover. |
| **Mack** | API integrations, MCP servers, webhooks, automations. |
| **Silas** | Structure, frontmatter integrity, imports from other note apps. |
| **Felix** | Frontend development. |
| **Vex** | Security review. Nothing with an integration ships without him. |
| **Vera** | QA and accessibility. Nothing visual ships without her. |
| **Iris** | Owns the design system. |
| **Charta** | Infographics, slides, diagrams. |
| **Pixel** | Image generation and visual finishing. |

**An orange-and-black Obsidian theme.** Wranglitdark. Colour, type and icons only,
with every text pairing measured against WCAG 2.2 AA — not estimated.

**Rules that are written down.** Naming conventions, frontmatter schemas, standard
procedures and multi-agent workstreams all live in `Team Knowledge/` as files you
can read and change.

---

## Getting started

You need a file-capable agent — one that reads **and writes** files on disk.
Claude Code, Codex CLI, Gemini CLI or Cursor. A chat-only web tool cannot run this.

1. Download or clone this folder.
2. Open your agent inside it.
3. Say: **"Initialize yourself inside this folder. Read ADAPTER-PROMPT.md and follow it to set yourself up."**

It reads the file itself. You do not paste anything.

What happens next:

- It asks your first name and personalizes the vault.
- It offers to switch on local version history — a time machine for the folder.
  Everything stays on your machine.
- It binds the twelve specialists to your tool.
- It interviews you for about five minutes and files what you tell it.
- It introduces itself as Larry, and you are running.

Then open the same folder in Obsidian and enable the Wranglitdark theme under
Settings → Appearance.

---

## Add Jarvis, a voice butler (optional)

Once the vault is running, you can build **Jarvis** on top of it: a voice assistant
that shows the vault as a 3D galaxy of your notes, answers questions from them out
loud, reads your Outlook calendar and email, and hands work to Larry's team.
You build your own copy by pasting twelve prompts into the Claude desktop app.
No code to download and no terminal.

The guide is in `Jarvis Guide/`. Open `jarvis-setup-guide.html` in your browser:
fill in your details once and every prompt updates with your own names and folders.
The same steps are in `Jarvis Guide/README.md` if you would rather read them on GitHub.

Jarvis is an add-on. Unlike the vault itself, it makes network calls (public CDNs,
your browser's speech recognition, and Claude Code on your subscription).

---

## How you actually use it

Talk to it. The triggers are plain English, not commands.

| You say | What happens |
|---|---|
| "Had a thought about the Hendricks proposal…" | Penn files it into today's journal and links the people involved |
| "File this meeting" + a transcript | The meeting note is written, new contacts are stubbed, and every action item becomes its own note in `Actions/` |
| "Remember this" | It goes into the session log as team memory |
| "Close session" | Larry writes the session log, checks every link, and fixes what drifted |
| "Can the team build a React app?" | Nolan hires the specialist for it. The answer is never "no" |
| "Import my Notion export" | Silas runs the import workstream |

---

## The rules it runs on

Three that matter most:

**One fact, one file.** If something is true, it is written down once. Everywhere
else links to it. No copy-paste, ever. Larry enforces this at session close.

**The local file wins.** If `AGENTS.md` in this folder says one thing and the
model's general training says another, the folder wins.

**Larry never does the work.** He routes it to the specialist whose contract covers
it, then reports back. That separation is what stops one generic assistant from
being mediocre at twelve jobs.

The full contract is `AGENTS.md` at the root. Read it — it is the system.

---

## Making it yours

- **Rename it.** Wranglit is a placeholder. Find and replace.
- **Rebrand the theme.** `GL-003-design-system.md` §9 walks through it. Re-run the
  contrast check when you swap the colours — the safe text steps depend on the hue.
- **Change the rules.** Everything in `Team Knowledge/Guidelines/` is yours to edit.
- **Add a specialist.** Say so. Nolan runs `SOP-001` and writes the contract.

---

## What is not in here

No telemetry. No network calls the system makes on its own. No account, no sign-in,
no cloud. If you want an off-machine backup later, that is your deliberate choice —
use a **private** repository, because this folder will contain personal data.

---

## Folder map

```
AGENTS.md           the contract — read this first
ADAPTER-PROMPT.md   first-run activation
CLAUDE.md           tool pointer for Claude Code

PKM/                your knowledge
  My Life/            Key Elements, Projects, Goals, Habits, Topics
  CRM/                People, Organizations, Meetings
  Journal/            daily entries, nested by year and month
  Documents/          passport, contracts, identity files
  Images/

Actions/            one note per action item
Deliverables/       work that belongs to no project
Team Inbox/         drop raw inputs here for filing

Team/               one folder per specialist, each with its contract
Team Knowledge/     SOPs, Workstreams, Guidelines, Templates, session logs
Expansions/         optional add-on packs (ships empty)
Jarvis Guide/       optional: build a voice assistant over the vault
```
