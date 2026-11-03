"""One-time Jarvis setup, run by Claude during install (see INSTALL-JARVIS.md in the vault).

    python setup.py [--name "First name"] [--no-start]

Run from the vault's hidden `.jarvis-app` folder. It:
  1. copies the app next to the vault:  <install>/app   (the vault is <install>/<vault folder>)
  2. writes app/config.json with the vault path and no keys
  3. lets an embedded (portable) Python find the app's own files
  4. builds the note index and the galaxy from the vault
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
VAULT = os.path.dirname(SRC)
INSTALL = os.path.dirname(VAULT)
APP = os.path.join(INSTALL, "app")
APP_FILES = ["server.py", "build.py", "approval_mcp.py", "launch.py", os.path.join("viewer", "index.html")]
DEFAULT_CONFIG = {"model": "claude-sonnet-5-5", "job_model": "claude-opus-5-5", "agent_permissions": "auto"}


def say(msg):
    print("[setup] " + msg, flush=True)


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
  $l = $s.CreateShortcut((Join-Path $dir 'Jarvis.lnk'))
  $l.TargetPath = $env:J_PY
  $l.Arguments = '"' + $env:J_LAUNCH + '"'
  $l.WorkingDirectory = $env:J_APP
  $l.Description = 'Start Jarvis'
  $l.Save()
}
"""
    env = dict(os.environ, J_PY=pythonw(), J_LAUNCH=os.path.join(APP, "launch.py"), J_APP=APP)
    subprocess.run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", ps], env=env, check=True)
    say("Shortcut 'Jarvis' added to the desktop and the Start menu.")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--name", default="")
    ap.add_argument("--no-start", action="store_true")
    ap.add_argument("--no-shortcuts", action="store_true")
    a = ap.parse_args()
    copy_app()
    write_config()
    fix_embedded_python()
    build_index()
    record_name(a.name)
    if not a.no_shortcuts:
        make_shortcuts()
    if not a.no_start:
        subprocess.run([sys.executable, os.path.join(APP, "launch.py")], cwd=APP, check=True)
    say("Done. Jarvis is ready.")


if __name__ == "__main__":
    main()
