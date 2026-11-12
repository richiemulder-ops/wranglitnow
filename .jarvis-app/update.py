"""Halo updates from GitHub. Standard library only.

check()  compares this install's VERSION.json with the one on GitHub (cached for a few hours).
apply()  downloads the repository, takes only its .jarvis-app folder, and copies the app files
         into the vault's .jarvis-app and into this app folder. config.json, data/ and the notes
         in the vault are never touched. The caller restarts the server afterwards.
"""
import io
import json
import os
import py_compile
import shutil
import tempfile
import time
import urllib.request
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = "richiemulder-ops/wranglitnow"
BRANCH = "main"
RAW_VERSION = f"https://raw.githubusercontent.com/{REPO}/{BRANCH}/.jarvis-app/VERSION.json"
ZIP_URL = f"https://github.com/{REPO}/archive/refs/heads/{BRANCH}.zip"
APP_FILES = ["server.py", "build.py", "semantic.py", "approval_mcp.py", "launch.py", "setup.py", "update.py",
             "VERSION.json", os.path.join("viewer", "index.html"),
             os.path.join("viewer", "jarvis.ico")]
CHECK_EVERY = 24 * 3600   # GitHub is asked when Halo starts, then once a day; "update yourself" asks at once
RETRY_AFTER = 10 * 60     # a failed check (offline at start-up) tries again soon, not a day later
_cache = {"at": 0, "remote": None, "problem": None}


def _key(v):
    """'2026.11.05.1' -> (2026, 11, 5, 1); anything unreadable sorts first."""
    try:
        return tuple(int(p) for p in str(v).split("."))
    except ValueError:
        return (0,)


def local_version():
    try:
        with open(os.path.join(HERE, "VERSION.json"), encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return {"version": "0", "notes": []}


def _fetch(url, timeout):
    req = urllib.request.Request(url, headers={"User-Agent": "Jarvis-updater", "Cache-Control": "no-cache"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def _notes_since(remote, current):
    """Notes for every version newer than `current`, newest first, so one update lists all it brings."""
    history = remote.get("history")
    if not history:
        return remote.get("notes", [])
    return [n for v in history if _key(v.get("version")) > _key(current) for n in v.get("notes", [])]


def check(force=False):
    wait = RETRY_AFTER if _cache["problem"] else CHECK_EVERY
    if force or time.time() - _cache["at"] > wait:
        try:
            _cache["remote"] = json.loads(_fetch(f"{RAW_VERSION}?t={int(time.time())}", 10))
            _cache["problem"] = None
        except (OSError, ValueError) as e:
            _cache["problem"] = f"Couldn't reach GitHub ({e.__class__.__name__})."
        _cache["at"] = time.time()
    here, there = local_version(), _cache["remote"] or {}
    newer = bool(there) and _key(there.get("version")) > _key(here.get("version"))
    return {"current": here.get("version"), "latest": there.get("version"), "available": newer,
            "notes": _notes_since(there, here.get("version")) if newer else [],
            "problem": _cache["problem"]}   # the page treats an "error" key as a failed call


def apply(vault):
    """Download and install the latest app files. Returns the new version; raises on any problem
    before a single installed file has been changed."""
    data = _fetch(ZIP_URL, 90)
    with tempfile.TemporaryDirectory() as tmp:
        with zipfile.ZipFile(io.BytesIO(data)) as z:
            # "<repo>-main/.jarvis-app/...": take the prefix from any file under it (zips needn't list folders)
            hit = next((n for n in z.namelist() if "/.jarvis-app/" in n), None)
            if not hit:
                raise ValueError("The download has no .jarvis-app folder.")
            prefix = hit[:hit.index("/.jarvis-app/") + len("/.jarvis-app/")]
            for name in z.namelist():
                if not name.startswith(prefix) or name.endswith("/"):
                    continue
                rel = os.path.normpath(name[len(prefix):])
                if rel.startswith("..") or os.path.isabs(rel):
                    raise ValueError("Unexpected file path in the download.")
                dest = os.path.join(tmp, rel)
                os.makedirs(os.path.dirname(dest), exist_ok=True)
                with z.open(name) as src, open(dest, "wb") as out:
                    shutil.copyfileobj(src, out)
        missing = [f for f in APP_FILES if not os.path.isfile(os.path.join(tmp, f))]
        if missing:
            raise ValueError("The download is missing " + ", ".join(missing) + ".")
        for f in APP_FILES:
            if f.endswith(".py"):
                py_compile.compile(os.path.join(tmp, f), doraise=True, cfile=os.path.join(tmp, "check.pyc"))
        new = json.load(open(os.path.join(tmp, "VERSION.json"), encoding="utf-8"))
        # Keep the vault's own copy current, so setup.py can be re-run from it at any time.
        target = os.path.join(vault, ".jarvis-app")
        for root, _, files in os.walk(tmp):
            for name in files:
                if name == "check.pyc":
                    continue
                src = os.path.join(root, name)
                dest = os.path.join(target, os.path.relpath(src, tmp))
                os.makedirs(os.path.dirname(dest), exist_ok=True)
                shutil.copy2(src, dest)
        for f in APP_FILES:
            os.makedirs(os.path.dirname(os.path.join(HERE, f)), exist_ok=True)
            shutil.copy2(os.path.join(tmp, f), os.path.join(HERE, f))
    _cache["at"] = 0
    return new.get("version")
