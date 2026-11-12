"""One-time Jarvis setup, run by Claude during install (see INSTALL-JARVIS.md in the vault).

    python setup.py [--name "First name"] [--vault <knowledge folder>] [--install <Jarvis folder>] [--no-start]

Jarvis is two folders: the app (the harness) in its own Jarvis folder, and your knowledge folder
(the vault: plain markdown notes, which can live anywhere, OneDrive included). The app only knows
the vault through the "vault" entry in app/config.json.

Run from the vault's hidden `.jarvis-app` folder. It:
  1. copies the app into the Jarvis folder:  <install>/app
     (--install; by default the folder recorded by an earlier setup, else the folder above the vault)
  2. writes app/config.json with the vault path (--vault; by default the folder above this script) and no keys
  3. lets an embedded (portable) Python find the app's own files
  4. builds the note index and the galaxy from the vault
     (and installs the meaning-search add-on, fastembed, when it can)
  5. records the user's first name in the vault (PKM/.user.yaml) when --name is given
  6. puts a "Jarvis" shortcut on the desktop and in the Start menu
  7. starts Jarvis and opens it in the browser (unless --no-start)

Safe to run again: it updates the app files and keeps config.json and data/.
Standard library only.
"""
import argparse
import glob
import json
import os
import shutil
import subprocess
import sys

SRC = os.path.dirname(os.path.abspath(__file__))          # <vault>/.jarvis-app
VAULT = os.path.dirname(SRC)                              # main() may point these elsewhere
INSTALL = os.path.dirname(VAULT)
APP = os.path.join(INSTALL, "app")
WHERE = "install.json"   # in <vault>/.jarvis-app: the Jarvis folder this vault was set up with
APP_FILES = ["server.py", "build.py", "semantic.py", "approval_mcp.py", "launch.py", "setup.py", "update.py", "VERSION.json",
             os.path.join("viewer", "index.html"),
             os.path.join("viewer", "jarvis.ico"), os.path.join("viewer", "halo.ico")]
DEFAULT_CONFIG = {"model": "claude-sonnet-5-5", "job_model": "claude-opus-5-5", "agent_permissions": "auto"}


def say(msg):
    print("[setup] " + msg, flush=True)


def locate(vault, install):
    """Work out the vault and the Jarvis folder. Re-running setup with no options reuses the Jarvis
    folder recorded last time, so it never makes a second copy of the app beside the vault."""
    global VAULT, INSTALL, APP
    VAULT = os.path.abspath(vault) if vault else VAULT
    if not install:
        try:
            with open(os.path.join(VAULT, ".jarvis-app", WHERE), encoding="utf-8") as f:
                install = (json.load(f) or {}).get("jarvis")
        except (OSError, ValueError, AttributeError):
            install = None
    INSTALL = os.path.abspath(install or os.path.dirname(VAULT))
    APP = os.path.join(INSTALL, "app")
    if not os.path.isdir(VAULT):
        sys.exit(f"[setup] Knowledge folder not found: {VAULT}")
    if os.path.normcase(APP + os.sep).startswith(os.path.normcase(VAULT + os.sep)):
        sys.exit("[setup] The Jarvis folder can't be inside the knowledge folder. Pick a folder outside it.")
    say(f"Jarvis folder: {INSTALL}")
    say(f"Knowledge folder: {VAULT}")


def remember_install():
    d = os.path.join(VAULT, ".jarvis-app")
    if os.path.isdir(d):
        with open(os.path.join(d, WHERE), "w", encoding="utf-8") as f:
            json.dump({"jarvis": INSTALL}, f, indent=2)


def copy_app():
    os.makedirs(os.path.join(APP, "viewer"), exist_ok=True)
    os.makedirs(os.path.join(APP, "data"), exist_ok=True)
    for rel in APP_FILES:
        shutil.copy2(os.path.join(SRC, rel), os.path.join(APP, rel))
    say(f"App files copied to {APP}")


def write_config():
    path = os.path.join(APP, "config.json")
    cfg = {}
    if os.path.isfile(path):
        try:
            with open(path, encoding="utf-8") as f:
                cfg = json.load(f) or {}
        except (OSError, ValueError):
            cfg = {}
    for k, v in DEFAULT_CONFIG.items():
        cfg.setdefault(k, v)
    cfg["vault"] = VAULT
    with open(path, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2)
    say("Settings saved (no keys stored).")


def fix_embedded_python():
    """A portable Python reads its search path from pythonXY._pth and ignores the script's own
    folder. Add the app folder so its scripts can always find each other."""
    home = os.path.dirname(sys.executable)
    for pth in glob.glob(os.path.join(home, "python*._pth")):
        with open(pth, encoding="utf-8") as f:
            lines = f.read().splitlines()
        if APP not in lines:
            lines.insert(1, APP)
            with open(pth, "w", encoding="utf-8") as f:
                f.write("\n".join(lines) + "\n")
            say("Portable Python pointed at the app folder.")


def build_index():
    say("Reading your notes (a few seconds)...")
    subprocess.run([sys.executable, os.path.join(APP, "build.py"), VAULT], cwd=APP, check=True)


def meaning_search():
    """Install the add-on behind meaning search (fastembed). Jarvis also does this itself in the
    background if it is missing, so a failure here never stops the install."""
    say("Adding meaning search, so Jarvis finds notes even in different words (a minute or two)...")
    try:
        sys.path.insert(0, APP)
        import semantic
        ok = semantic.ensure_installed(log=lambda m: None)
    except Exception:
        ok = False
    say("Meaning search ready." if ok else "Meaning search will finish setting itself up when Jarvis starts.")


def record_name(name):
    """The vault's own first-run steps look for PKM/.user.yaml; Larry fills in {{USER_NAME}}."""
    name = " ".join(name.split())[:60]
    if not name:
        return
    path = os.path.join(VAULT, "PKM", ".user.yaml")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if not os.path.isfile(path):
        with open(path, "w", encoding="utf-8") as f:
            f.write(f"first_name: {name}\n")
    cfg_path = os.path.join(APP, "config.json")
    with open(cfg_path, encoding="utf-8") as f:
        cfg = json.load(f)
    cfg.setdefault("user_name", name)
    with open(cfg_path, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2)
    say(f"Name recorded: {name}")


def pythonw():
    w = os.path.join(os.path.dirname(sys.executable), "pythonw.exe")
    return w if os.path.isfile(w) else sys.executable


def make_shortcuts():
    if os.name != "nt":
        say("Not Windows: start Jarvis with  python app/launch.py")
        return
    ps = r"""
$s = New-Object -ComObject WScript.Shell
foreach ($dir in @([Environment]::GetFolderPath('Desktop'), (Join-Path $env:APPDATA 'Microsoft\Windows\Start Menu\Programs'))) {
  # Halo was called Jarvis: a re-run replaces this install's old shortcut instead of adding a second.
  $old = Join-Path $dir 'Jarvis.lnk'
  if (Test-Path $old) {
    if ($s.CreateShortcut($old).Arguments -like ('*' + $env:J_LAUNCH + '*')) { Remove-Item -LiteralPath $old }
  }
  $l = $s.CreateShortcut((Join-Path $dir 'Halo.lnk'))
  $l.TargetPath = $env:J_PY
  $l.Arguments = '"' + $env:J_LAUNCH + '"'
  $l.WorkingDirectory = $env:J_APP
  $l.Description = 'Start Halo'
  $l.IconLocation = $env:J_ICON + ',0'
  $l.Save()
}
"""
    env = dict(os.environ, J_PY=pythonw(), J_LAUNCH=os.path.join(APP, "launch.py"), J_APP=APP, J_ICON=os.path.join(APP, "viewer", "halo.ico"))
    subprocess.run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", ps], env=env, check=True)
    say("Shortcut 'Halo' added to the desktop and the Start menu.")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--name", default="")
    ap.add_argument("--vault", default="", help="the knowledge folder (default: the folder this .jarvis-app is in)")
    ap.add_argument("--install", default="", help="the Jarvis folder; the app goes in <install>/app")
    ap.add_argument("--no-start", action="store_true")
    ap.add_argument("--no-shortcuts", action="store_true")
    a = ap.parse_args()
    locate(a.vault, a.install)
    copy_app()
    remember_install()
    write_config()
    fix_embedded_python()
    build_index()
    meaning_search()
    record_name(a.name)
    if not a.no_shortcuts:
        make_shortcuts()
    if not a.no_start:
        subprocess.run([sys.executable, os.path.join(APP, "launch.py")], cwd=APP, check=True)
    say("Done. Jarvis is ready.")


if __name__ == "__main__":
    main()
