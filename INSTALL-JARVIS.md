# Install Jarvis: instructions for Claude

The person installing pasted something like *"Install Jarvis for me from github.com/richiemulder-ops/wranglitnow"* into the Claude desktop app. **You (Claude) do the whole install.** They should only need to answer three questions and, at most, sign in once in their browser.

## How Jarvis is laid out (read this first)

Jarvis is two separate folders:

- **The Jarvis folder** (`ROOT`): the program. `ROOT\app` holds the local web server, the page, `config.json` and `data\` (search index, chat history), and `ROOT\python` holds a private Python if the PC needs one. Nothing of theirs lives here.
- **The knowledge folder** (`KNOWLEDGE`): their notes, as plain markdown, plus the team (`AGENTS.md`, `Team\`, `Team Knowledge\`) and a spare copy of the program in `.jarvis-app\`. It can be anywhere: Documents, OneDrive, a folder inside OneDrive, a synced SharePoint folder.

Jarvis finds the knowledge folder through the `vault` entry in `ROOT\app\config.json`, which `setup.py` writes. The two folders don't need to be next to each other, but **the Jarvis folder must not be inside the knowledge folder**.

This repository is the starter knowledge folder, with the program in `.jarvis-app/`. Obsidian is not needed at any point.

## How to behave

- Talk to them in short, plain sentences. No jargon, no code in your messages unless something fails and you need them to click something.
- Do every step yourself with your tools. Never ask them to open a terminal or type a command.
- Before you start, tell them in one line what will happen: "I'll install Jarvis in its own folder, set up your knowledge folder, and open it. About five minutes."
- Nothing needs an admin password. Nothing outside the two folders changes except two shortcuts (desktop and Start menu) and, if missing, Claude Code.
- **Never overwrite or delete anything already in their knowledge folder.**
- If a step fails, use the fix listed under it. If that also fails, tell them in one sentence what went wrong and what you need from them.

This guide is for **Windows**. On a Mac, follow the same steps with the notes marked *Mac*.

**Already installed?** If they asked you to *update* Jarvis, skip to [Update an existing install](#update-an-existing-install) at the end.

---

## Step 1. Ask three questions (in one message)

1. "What's your first name?" (Jarvis and the team will use it.)
2. "I'll install the Jarvis program in its own folder, **C:\Users\\<you>\Jarvis**. Is that OK, or would you like it somewhere else?"
3. "Where should your **knowledge folder** be? That's where all your notes live, and Jarvis links to it. It can be a new folder (I'd suggest **Documents\My Knowledge**), a folder in OneDrive so it's backed up, or a folder you already have notes in."

Call the answers `NAME`, `ROOT` and `KNOWLEDGE`. Use full paths:

- `ROOT` default: `$env:USERPROFILE\Jarvis`. Prefer a folder outside OneDrive: the program and its index change constantly and don't need syncing. If they want it in OneDrive anyway, that's fine.
- `KNOWLEDGE` default: `<Documents>\My Knowledge`, where `<Documents>` comes from PowerShell `[Environment]::GetFolderPath('MyDocuments')` (it is often inside OneDrive already). If they name a OneDrive folder, find OneDrive with `$env:OneDrive` (personal) or `$env:OneDriveCommercial` (work or school), and the folder they mean inside it. If you can't tell which folder they mean, list the likely ones and ask.

Then check:

- `ROOT` must not be inside `KNOWLEDGE`. If it is, suggest `$env:USERPROFILE\Jarvis` instead.
- If `ROOT\app\config.json` already exists, Jarvis is already installed there. Ask whether to update it ([Update an existing install](#update-an-existing-install)) or pick another folder.
- Look at `KNOWLEDGE` and decide which case it is (you'll need this in Step 4):
  - **New**: the folder doesn't exist yet, or is empty.
  - **Existing team folder**: it already has `AGENTS.md` and a `Team` folder (an earlier Jarvis or Wranglit install).
  - **Existing notes**: it has other files. Tell them: "Your files stay exactly as they are. I'll add the team's folders beside them, and your notes will show up in Jarvis."

If `KNOWLEDGE` is in OneDrive, tell them: "Right-click that folder in File Explorer and choose **Always keep on this device**, so Jarvis can read your notes instantly." Carry on; you don't need to wait.

## Step 2. Python

Check, in order: `python --version`, then `py -3 --version`. Version **3.10 or newer** is fine: call that command `PY` and go to Step 3. (Ignore the Microsoft Store stub that only prints an install message: it is not Python.)

If there is no suitable Python, install the official **portable** Python from python.org inside the Jarvis folder. No admin rights needed, and nothing else on the PC changes:

```powershell
$root = "<ROOT>"
New-Item -ItemType Directory -Force "$root\python" | Out-Null
$arch = if ($env:PROCESSOR_ARCHITECTURE -eq 'ARM64') { 'arm64' } else { 'amd64' }
Invoke-WebRequest "https://www.python.org/ftp/python/3.12.10/python-3.12.10-embed-$arch.zip" -OutFile "$root\python.zip"
Expand-Archive "$root\python.zip" "$root\python" -Force
Remove-Item "$root\python.zip"
& "$root\python\python.exe" --version
```

Then `PY` is `<ROOT>\python\python.exe`. Tell them: "Your PC didn't have Python, so I've put a private copy inside the Jarvis folder."

- Fails to download: antivirus or a proxy is blocking it. Ask them to allow python.org, or to install Python from https://www.python.org/downloads/ (tick *Add python.exe to PATH*), then carry on.
- *Mac:* `python3 --version` usually works. If not, ask them to install Python from python.org (double-click the downloaded file) and carry on.

## Step 3. Claude Code (the engine Jarvis runs on)

Check `claude --version`, and if that isn't found, `"$env:USERPROFILE\.local\bin\claude.exe" --version`.

If it isn't installed, use Anthropic's official installer:

```powershell
irm https://claude.ai/install.ps1 | iex
```

Then check that Claude Code is signed in **on its own**. It runs on their Claude subscription, so there is no API key and no extra cost.

Important: your shell runs inside the Claude desktop app, which passes its own sign-in down through `ANTHROPIC_*` and `CLAUDE_CODE_*` settings. A plain `claude -p` here would borrow that sign-in and pass, and then Jarvis would fail with "Not logged in" the first time it is started from the desktop shortcut (after a restart, say). So clear those settings first, in the same command:

```powershell
Get-ChildItem env: | Where-Object { $_.Name -match '^(ANTHROPIC_|CLAUDE_CODE_|CLAUDECODE$)' } | Remove-Item; claude auth status
```

If it shows `"loggedIn": true`, carry on. If it shows `false` (or an error), open a sign-in window for them, with the same settings cleared:

```powershell
Start-Process powershell -ArgumentList '-NoExit', '-Command', "Get-ChildItem env: | Where-Object { `$_.Name -match '^(ANTHROPIC_|CLAUDE_CODE_|CLAUDECODE$)' } | Remove-Item; claude auth login"
```

Tell them: "A window has opened and your browser will ask you to sign in to your Claude account. Sign in, then close that window and tell me when you're done." Then run the check again and don't go on until it says `"loggedIn": true`.

## Step 4. Download and fill the knowledge folder

Download the repository as a zip into a temporary folder, so no Git is needed:

```powershell
$tmp = Join-Path $env:TEMP "jarvis-download"
Remove-Item $tmp, "$tmp.zip" -Recurse -Force -ErrorAction SilentlyContinue
Invoke-WebRequest "https://github.com/richiemulder-ops/wranglitnow/archive/refs/heads/main.zip" -OutFile "$tmp.zip"
Expand-Archive "$tmp.zip" $tmp -Force
$src = "$tmp\wranglitnow-main"
$k = "<KNOWLEDGE>"
New-Item -ItemType Directory -Force $k | Out-Null
```

- 404 or a sign-in page: the repository is private. Tell them: "The download is locked. Ask the person who sent you this to share it with you," and stop.

Then copy, depending on the case from Step 1. Robocopy exit codes below 8 mean success.

- **New:** copy everything.

  ```powershell
  robocopy $src $k /E /NFL /NDL /NJH /NJS
  ```

- **Existing team folder:** only refresh the program copy. Leave everything else alone.

  ```powershell
  robocopy "$src\.jarvis-app" "$k\.jarvis-app" /E /NFL /NDL /NJH /NJS
  ```

- **Existing notes:** copy only files that aren't there yet. `/XC /XN /XO` skips every file that already exists, so nothing of theirs is overwritten.

  ```powershell
  robocopy $src $k /E /XC /XN /XO /NFL /NDL /NJH /NJS
  ```

Then clean up: `Remove-Item $tmp, "$tmp.zip" -Recurse -Force`

## Step 5. Set up Jarvis

Run setup from the program copy in the knowledge folder, telling it where the Jarvis folder goes:

```powershell
& "<PY>" "<KNOWLEDGE>\.jarvis-app\setup.py" --name "<NAME>" --install "<ROOT>"
```

This puts the program in `<ROOT>\app`, writes `config.json` pointing at the knowledge folder (no keys), records the Jarvis folder in `<KNOWLEDGE>\.jarvis-app\install.json` (so running setup again later reuses it), builds the note index, adds a **Jarvis** shortcut to the desktop and the Start menu, starts Jarvis and opens it in the browser.

- "The Jarvis folder can't be inside the knowledge folder": pick a `ROOT` outside `KNOWLEDGE` and run it again.
- It reports the server didn't start: read `<ROOT>\app\data\server.log`, fix what it says, then run `& "<PY>" "<ROOT>\app\launch.py"`.
- Port 4700 is in use: something else is running there. Ask them to close it, or restart the PC, then run the launcher again.
- *Mac:* no shortcuts are made. Start Jarvis with `python3 "<ROOT>/app/launch.py"`.

## Step 6. Wake up the team (first run in the knowledge folder)

Skip this step for an **existing team folder**: its team is already set up.

Otherwise, the knowledge folder has its own one-time activation, which personalises the files and connects the specialists. Run it now, inside the knowledge folder:

```powershell
cd "<KNOWLEDGE>"
claude -p "Read ADAPTER-PROMPT.md and run activation now. The user's first name is <NAME>. They have already agreed to the whole setup, so use that single consent and do not ask again. Skip the Cockpit build and the local git step if they need anything that isn't installed. Do not move, rename or change any file that was in this folder before today. Reply with a short summary." --permission-mode acceptEdits
```

It takes a minute or two. If it stops to ask a question, answer it yourself from what you know (their name, the knowledge folder) or skip that part. Then confirm that `.claude\agents\` in the knowledge folder contains the specialist files.

## Step 7. Hand over

Tell them, in about four lines:

- "Jarvis is open in your browser. **Click anywhere to wake him**, and he'll walk you through a short welcome (voice, colours, your team, Outlook)."
- "Your notes live in <KNOWLEDGE>. Jarvis is installed separately in <ROOT> and just links to it."
- "Next time, just double-click **Jarvis** on your desktop."
- "Use Chrome or Edge: they have the best voices."

That's it. Don't list what you did unless they ask. Don't mention Obsidian unless they ask; if they do, say it's optional: they can open the knowledge folder as a vault in Obsidian if they like.

---

### Later

- **Update Jarvis:** Jarvis shows an **Update** tile in its top bar when a new version is out; one click installs it. It replaces program files only (in `ROOT\app` and `KNOWLEDGE\.jarvis-app`), never notes, `config.json` or `data\`. For older installs without that tile, see below.
- **Stop Jarvis:** run `& "<PY>" "<ROOT>\app\launch.py" --stop`, or restart the PC.
- **Move the knowledge folder:** stop Jarvis, move the folder, then run setup from its new place, pointing at the same Jarvis folder: `& "<PY>" "<NEW KNOWLEDGE>\.jarvis-app\setup.py" --install "<ROOT>"`. It updates `config.json`, rebuilds the index and restarts Jarvis. Settings and chat history stay.
- **Rerun the welcome:** in the browser console, run `JARVIS_ONBOARD()`.
- **Uninstall:** stop Jarvis, then delete the `<ROOT>` folder and the two Jarvis shortcuts. That removes the program, including the private Python copy. The knowledge folder is theirs: leave it unless they ask you to delete it too.

---

## Update an existing install

For someone who already has Jarvis. Their notes and settings must not change: only the program files are replaced.

1. Find the two folders. The desktop **Jarvis** shortcut points at `<ROOT>\app\launch.py`, and its target is the Python to use (`PY`; if it's `pythonw.exe`, use `python.exe` from the same folder). The `vault` entry in `<ROOT>\app\config.json` is the knowledge folder (`KNOWLEDGE`). Older installs put it at `<ROOT>\My Vault`.
2. Stop Jarvis: `& "<PY>" "<ROOT>\app\launch.py" --stop` (fine if it says it isn't running).
3. Download the latest program into a temporary folder and copy only its `.jarvis-app` over the old one:

```powershell
$k = "<KNOWLEDGE>"
$tmp = Join-Path $env:TEMP "jarvis-update"
Remove-Item $tmp, "$tmp.zip" -Recurse -Force -ErrorAction SilentlyContinue
Invoke-WebRequest "https://github.com/richiemulder-ops/wranglitnow/archive/refs/heads/main.zip" -OutFile "$tmp.zip"
Expand-Archive "$tmp.zip" $tmp -Force
Copy-Item "$tmp\wranglitnow-main\.jarvis-app\*" "$k\.jarvis-app" -Recurse -Force
Remove-Item $tmp, "$tmp.zip" -Recurse -Force
```

4. Run setup again, naming the Jarvis folder it already uses (no name needed; it keeps `config.json` and `data\`, and restarts Jarvis): `& "<PY>" "$k\.jarvis-app\setup.py" --install "<ROOT>"`
5. Tell them: "Jarvis is updated and open again. From now on, an **Update** tile appears in the top bar whenever there's a new version: one click and it's done."

Never touch anything else in the knowledge folder: no notes, no `.claude` files, no `Team` folders.
