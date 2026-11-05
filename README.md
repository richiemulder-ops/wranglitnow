# Jarvis

A voice assistant with an AI team behind it, running from folders on your own PC.

You talk to Jarvis in your browser. It answers from your notes, reads your Outlook
calendar and email, and hands real work to a team of twelve AI specialists who read
and write files in your knowledge folder. Everything it knows is plain markdown files
in a folder you choose. There's no database and no Jarvis account.

---

## How it works

Jarvis is two folders and an engine.

```
 Jarvis folder  (e.g. C:\Users\you\Jarvis)          Knowledge folder  (anywhere you like)
 ─────────────────────────────────────────          ─────────────────────────────────────
 app\           the Jarvis program                  PKM\            your notes, CRM, journal
   config.json  says where your knowledge  ──────►  Actions\        one note per action item
                folder is                           Deliverables\   finished work
   data\        search index, chat history          Team Inbox\     drop files here to be filed
   viewer\      the page you see in the browser     Team\           the twelve specialists
 python\        private Python (only if your PC     Team Knowledge\ rules, procedures, templates
                didn't have one)                    AGENTS.md       the team's contract
                                                    .jarvis-app\    a spare copy of the program

                         Engine: Claude Code, signed in to your Claude account
```

**The Jarvis folder is the harness.** It holds the program and nothing else of yours.
The installer puts it in its own folder, outside your notes. A small local web
server runs from it (only on your PC, at `http://localhost:4700`), and the **Jarvis**
shortcut on your desktop starts it and opens the page in your browser.

**The knowledge folder is yours.** It's where every note, contact, meeting, action
and deliverable lives, as markdown files you can open in any editor. It can be
anywhere on your PC: Documents, OneDrive, a folder inside OneDrive, or a SharePoint
folder synced through OneDrive. Jarvis finds it through one line in
`app\config.json`, so the two folders don't have to sit next to each other.

**Claude Code is the engine.** When you ask a question, Jarvis runs Claude Code on
your Claude subscription with the notes that matter. When you ask for work ("file
these meeting notes", "draft a reply to Sam"), the job goes to Larry, who hands it
to the right specialist. They work directly in your knowledge folder, and you watch
them do it in the **Current work** office view. Anything outside routine file work
comes to you as an approval card first.

This repository is the starter knowledge folder plus the program (in `.jarvis-app/`).
The installer copies it into place for you.

---

## Install (one prompt)

1. Install the **Claude desktop app** from claude.ai/download and sign in (Claude Pro or Max).
2. Open its **Code** tab and paste:

   > Install Jarvis for me from github.com/richiemulder-ops/wranglitnow

3. Answer three questions: your first name, where to put the Jarvis folder, and
   where your knowledge folder should be (a new folder, or one you already have, for
   example in OneDrive). Claude does the rest, including installing Python if your PC
   doesn't have it, and opens Jarvis in your browser.
4. Click to wake Jarvis. A short welcome sets your name, voice, colours and Outlook.

After that, double-click **Jarvis** on your desktop. Claude follows
[INSTALL-JARVIS.md](INSTALL-JARVIS.md). Windows is tested; Mac follows the same steps.

If you point it at a folder that already has your notes, nothing in it is
overwritten. The starter folders are added beside your files, and your existing
notes show up in Jarvis straight away.

### If your knowledge folder is in OneDrive

That works, and it gives you a backup for free. Two things help:

- Right-click the knowledge folder in File Explorer and choose **Always keep on this
  device**. Files that exist only in the cloud open slowly and can stall the team.
- Keep the Jarvis folder outside OneDrive (the installer suggests
  `C:\Users\<you>\Jarvis`). It's program files and a search index that change all the
  time and don't need syncing.

---

## What you can do with it

- **Ask anything about your notes**, by voice or typing. Answers are read aloud (Chrome
  or Edge have the best voices).
- **See your notes as a 3D galaxy**, with projects, people and meetings as clusters you
  can click into.
- **Hand over work.** "File today's meeting", "write me a document on…", "tidy the
  inbox". The team does it in your knowledge folder and the result opens on screen.
- **Watch the team work** in the Current work office: each specialist is a bot that
  walks between desks and machines as it works, and comes to the CEO's desk when it
  needs your OK.
- **Outlook, read only.** Today's meetings, a calendar for any span, and email search,
  once Microsoft 365 is connected in your Claude account. The team can put drafts in
  your Outlook Drafts folder. Nothing is ever sent for you.
- **Approvals.** Anything beyond routine file work in your knowledge folder comes to
  you as a plain-English card: what it will do, why, and Approve or Deny.
- **Updates.** When a new version is out, an **Update** tile appears in the top bar.
  One click replaces the program files. Your notes, settings and chat history aren't
  touched.

---

## The team

Twelve specialists. They're not twelve chatbots: they're twelve written contracts
(in `Team/`) that tell one model how to behave in twelve different jobs.

| | |
|---|---|
| **Larry** | Orchestrator. Every request lands here first. He routes, then reports back. He never does the work himself. |
| **Penn** | Captures what you say into the journal and your notes. |
| **Pax** | Researches with cross-source verification. |
| **Nolan** | Hires a thirteenth specialist when you need a role the twelve don't cover. |
| **Mack** | API integrations, MCP servers, webhooks, automations. |
| **Silas** | Structure, frontmatter integrity, imports from other note apps. |
| **Felix** | Frontend development. |
| **Vex** | Security review. Nothing with an integration ships without him. |
| **Vera** | QA and accessibility. Nothing visual ships without her. |
| **Iris** | Owns the design system. |
| **Charta** | Infographics, slides, diagrams. |
| **Pixel** | Image generation and visual finishing. |

### The rules they run on

**One fact, one file.** If something is true, it's written down once, and everything
else links to it. Larry checks this at the end of a session.

**The local file wins.** If `AGENTS.md` in your knowledge folder says one thing and the
model's general training says another, the folder wins.

**Larry never does the work.** He routes it to the specialist whose contract covers
it. That separation is what stops one generic assistant being mediocre at twelve jobs.

The full contract is `AGENTS.md` in the knowledge folder. Every rule, procedure and
template is in `Team Knowledge/` as a file you can read and change.

---

## Your knowledge folder

```
AGENTS.md           the team's contract: read this first
ADAPTER-PROMPT.md   the team's first-run activation (the installer runs it)
CLAUDE.md           pointer for Claude Code

PKM/                your knowledge
  My Life/            Key Elements, Projects, Goals, Habits, Topics
  CRM/                People, Organizations, Meetings
  Journal/            daily entries, by year and month
  Documents/          passport, contracts, identity files
  Images/

Actions/            one note per action item
Deliverables/       work that belongs to no project
Team Inbox/         drop raw inputs here for filing

Team/               one folder per specialist, each with its contract
Team Knowledge/     SOPs, Workstreams, Guidelines, Templates, session logs
Expansions/         optional add-on packs (ships empty)
.jarvis-app/        a copy of the Jarvis program, used to set it up again
```

Your life splits into Key Elements, Projects, Goals, Habits and Topics. People and
organizations live in a CRM. Meetings get filed, and their action items become notes
in `Actions/` automatically.

### Things you can say

| You say | What happens |
|---|---|
| "Had a thought about the Hendricks proposal…" | Penn files it into today's journal and links the people involved |
| "File this meeting" + a transcript | The meeting note is written, new contacts are added, and every action item becomes its own note |
| "Remember this" | It goes into the session log as team memory |
| "Can the team build a React app?" | Nolan hires the specialist for it |
| "Import my Notion export" | Silas runs the import |

### Making it yours

- **Change the rules.** Everything in `Team Knowledge/Guidelines/` is yours to edit.
- **Add a specialist.** Say so. Nolan writes the contract.
- **Move the knowledge folder.** Ask Claude to point Jarvis at the new place (see
  "Later" in [INSTALL-JARVIS.md](INSTALL-JARVIS.md)), or edit `vault` in
  `<Jarvis folder>\app\config.json` and restart Jarvis.

---

## What goes over the network

Your files stay on your PC (and in OneDrive, if that's where you put them). Jarvis
does make these calls:

- **Claude Code**, on your subscription: your questions, and the notes needed to
  answer them or do a job, go to Anthropic.
- **Speech recognition** in your browser: Chrome and Edge send what you say to Google
  or Microsoft to turn it into text.
- **Microsoft 365**, if you've connected it in your Claude account: calendar and email
  searches, read only, plus drafts the team places.
- **Updates**: every few hours Jarvis checks this GitHub repository for a newer version.
- **The page itself** loads a few public libraries (such as the 3D engine) from public
  CDNs.

No telemetry, and no Jarvis account.

---

## Stopping and uninstalling

- **Stop Jarvis:** restart the PC, or ask Claude to stop it.
- **Uninstall:** delete the Jarvis folder and the two Jarvis shortcuts (desktop and
  Start menu). Your knowledge folder is separate and stays exactly as it is. Delete it
  too only if you want your notes gone.

---

## Without Jarvis

The knowledge folder works on its own. Open it in any agent that can read and write
files (Claude Code, Codex CLI, Gemini CLI or Cursor) and talk to Larry there. On a
fresh folder, say: **"Initialize yourself inside this folder. Read ADAPTER-PROMPT.md
and follow it to set yourself up."** (The Jarvis installer already does this for you.)

To build your own Jarvis from scratch instead of installing this one, see
`Jarvis Guide/`.

---

## Obsidian (optional)

You don't need Obsidian. Jarvis and the team work on the plain files. If you like
reading and editing notes in Obsidian, open your knowledge folder as a vault there.
It comes with **Wranglitdark**, an orange-and-black theme with every text colour pair
checked against WCAG 2.2 AA: turn it on under Settings → Appearance. Jarvis's
**Open on desktop** button then opens notes in Obsidian, if Obsidian is your app for
`.md` files.
