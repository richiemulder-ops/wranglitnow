# Install Jarvis: instructions for Claude

The person installing pasted something like *"Install Jarvis for me from github.com/richiemulder-ops/wranglitnow"* into the Claude desktop app. **You (Claude) do the whole install.** They should only need to answer two questions and, at most, sign in once in their browser.

How to behave:

- Talk to them in short, plain sentences. No jargon, no code in your messages unless something fails and you need them to click something.
- Do every step yourself with your tools. Never ask them to open a terminal or type a command.
- Before you start, tell them in one line what will happen: "I'll download Jarvis and your notes vault, set up what it needs, and open it. About five minutes."
- Everything installs inside one folder in their Documents. Nothing needs an admin password, and nothing outside that folder changes except two shortcuts (desktop and Start menu) and, if missing, Claude Code.
- If a step fails, use the fix listed under it. If that also fails, tell them in one sentence what went wrong and what you need from them.

This guide is for **Windows**. On a Mac, follow the same steps with the notes marked *Mac*.

**Already installed?** If they asked you to *update* Jarvis, skip to [Update an existing install](#update-an-existing-install) at the end.

---

## Step 1. Ask two questions (in one message)

1. "What's your first name?" (Jarvis and the team will use it.)
2. "I'll install into **Documents\Jarvis**. Is that OK, or would you like it somewhere else?"

Call the answers `NAME` and `ROOT`. Find the real Documents folder with PowerShell `[Environment]::GetFolderPath('MyDocuments')` (it is often inside OneDrive). If `ROOT` already contains a `My Vault` folder, ask whether to update the existing install or pick a new folder. Never overwrite their notes.

## Step 2. Python

Check, in order: `python --version`, then `py -3 --version`. Version **3.10 or newer** is fine: call that command `PY` and go to Step 3. (Ignore the Microsoft Store stub that only prints an install message: it is not Python.)

If there is no suitable Python, install the official **portable** Python from python.org inside the install folder. No admin rights needed, and nothing else on the PC changes:

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

Then check that it is signed in to their Claude account. It runs on their subscription, so there is no API key and no extra cost:

```powershell
claude -p "Reply with the single word OK" --output-format text
```

If that says it isn't logged in, open a sign-in window for them:

```powershell
Start-Process powershell -ArgumentList '-NoExit', '-Command', 'claude'
```

Tell them: "A window has opened. Follow the sign-in it shows (it opens your browser), then close that window and tell me when you're done." Then run the check again.

## Step 4. Download the vault and Jarvis

Download the repository as a zip, so no Git is needed:

```powershell
$root = "<ROOT>"
Invoke-WebRequest "https://github.com/richiemulder-ops/wranglitnow/archive/refs/heads/main.zip" -OutFile "$root\jarvis.zip"
Expand-Archive "$root\jarvis.zip" "$root\_unzip" -Force
Move-Item "$root\_unzip\wranglitnow-main" "$root\My Vault"
Remove-Item "$root\_unzip", "$root\jarvis.zip" -Recurse -Force
```

- 404 or a sign-in page: the repository is still private. Tell them: "The download is locked. Ask the person who sent you this to share it with you," and stop.

## Step 5. Set up Jarvis

```powershell
& "<PY>" "<ROOT>\My Vault\.jarvis-app\setup.py" --name "<NAME>"
```

This copies the app to `<ROOT>\app`, saves its settings (no keys), builds the note index, adds a **Jarvis** shortcut to the desktop and the Start menu, starts Jarvis, and opens it in the browser.

- It reports the server didn't start: read `<ROOT>\app\data\server.log`, fix what it says, then run `& "<PY>" "<ROOT>\app\launch.py"`.
- Port 4700 is in use: something else is running there. Ask them to close it, or restart the PC, then run the launcher again.

## Step 6. Wake up the team (vault first run)

The vault has its own one-time activation, which personalises the files and connects the specialists. Run it now, in the vault folder:

```powershell
cd "<ROOT>\My Vault"
claude -p "Read ADAPTER-PROMPT.md and run activation now. The user's first name is <NAME>. They have already agreed to the whole setup, so use that single consent and do not ask again. Skip the Cockpit build and the local git step if they need anything that isn't installed. Reply with a short summary." --permission-mode acceptEdits
```

It takes a minute or two. If it stops to ask a question, answer it yourself from what you know (their name, the vault folder) or skip that part. Then confirm that `.claude\agents\` in the vault contains the specialist files.

## Step 7. Hand over

Tell them, in about three lines:

- "Jarvis is open in your browser. **Click anywhere to wake him**, and he'll walk you through a short welcome (voice, colours, your team, Outlook)."
- "Next time, just double-click **Jarvis** on your desktop."
- "Use Chrome or Edge: they have the best voices."

That's it. Don't list what you did unless they ask.

---

### Later

- **Update Jarvis:** Jarvis shows an **Update** tile in its top bar when a new version is out; one click installs it. For older installs without that tile, see below.
- **Stop Jarvis:** run `& "<PY>" "<ROOT>\app\launch.py" --stop`, or restart the PC.
- **Rerun the welcome:** in the browser console, run `JARVIS_ONBOARD()`.
- **Uninstall:** delete the `<ROOT>` folder and the two Jarvis shortcuts. That removes everything, including the private Python copy.

---

## Update an existing install

For someone who already has Jarvis. Their notes and settings must not change: only the app files are replaced.

1. Find the install. The desktop **Jarvis** shortcut points at `<ROOT>\app\launch.py`, and its target is the Python to use (`PY`; if it's `pythonw.exe`, use `python.exe` from the same folder). Or look for `Documents\Jarvis\app\config.json`: its `vault` entry is the vault folder.
2. Stop Jarvis: `& "<PY>" "<ROOT>\app\launch.py" --stop` (fine if it says it isn't running).
3. Download the latest app into a temporary folder and copy only its `.jarvis-app` over the old one:

```powershell
$root = "<ROOT>"; $vault = "<VAULT>"   # the vault folder, usually "$root\My Vault"
$tmp = Join-Path $env:TEMP "jarvis-update"
Remove-Item $tmp -Recurse -Force -ErrorAction SilentlyContinue
Invoke-WebRequest "https://github.com/richiemulder-ops/wranglitnow/archive/refs/heads/main.zip" -OutFile "$tmp.zip"
Expand-Archive "$tmp.zip" $tmp -Force
Copy-Item "$tmp\wranglitnow-main\.jarvis-app\*" "$vault\.jarvis-app" -Recurse -Force
Remove-Item $tmp, "$tmp.zip" -Recurse -Force
```

4. Run setup again (no name needed; it keeps `config.json` and `data\`, and restarts Jarvis): `& "<PY>" "$vault\.jarvis-app\setup.py"`
5. Tell them: "Jarvis is updated and open again. From now on, an **Update** tile appears in the top bar whenever there's a new version: one click and it's done."

Never touch anything else in the vault: no notes, no `.claude` files, no `Team` folders.
