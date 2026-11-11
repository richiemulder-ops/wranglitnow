"""Meaning-based search for Jarvis (level 3: "I searched different words than I wrote").

Each note is cut into overlapping passages and every passage gets a vector from a small local
model (BAAI/bge-small-en-v1.5 through fastembed, ~67 MB, CPU only; nothing leaves the machine).
server.py keeps the vectors up to date in the background (refresh_meaning) and blends meaning
matches with its keyword search.

Seamless on any install: when fastembed isn't there, ensure_installed() installs it in the
background (bootstrapping pip first on a portable Python). Until it's ready, or if it can't be
installed, Jarvis simply keeps using keyword search.
"""
import glob
import hashlib
import importlib
import json
import os
import site
import subprocess
import sys
import threading
import time
import urllib.request

# Quiet the model downloader's Windows symlink notice (read when it is imported).
os.environ.setdefault("HF_HUB_DISABLE_SYMLINKS_WARNING", "1")

HERE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(HERE, "data")
MODEL_DIR = os.path.join(DATA_DIR, "models")             # kept out of %TEMP%, which gets cleaned
VECTORS_FILE = os.path.join(DATA_DIR, "notes-vectors.npz")  # vectors + passage list in one file, so they always match
LOCK_FILE = os.path.join(DATA_DIR, "notes-vectors.lock")    # one build embeds at a time
SETUP_FILE = os.path.join(DATA_DIR, "meaning-setup.json")   # last install attempt, so a failure isn't retried all day
LOCK_STALE = 45 * 60
MODEL_NAME = "BAAI/bge-small-en-v1.5"
PACKAGE = "fastembed==0.9.1"
GET_PIP = "https://bootstrap.pypa.io/get-pip.py"
RETRY_INSTALL = 24 * 3600

CHUNK_CHARS = 1200      # about 300 tokens, inside the model's 512-token window
CHUNK_OVERLAP = 200
BATCH = 32
CHECKPOINT = 512        # passages embedded between progress saves

np = None
TextEmbedding = None
AVAILABLE = False


def _import():
    """Pick up fastembed (and numpy), including one installed since Jarvis started."""
    global np, TextEmbedding, AVAILABLE
    if AVAILABLE:
        return True
    importlib.invalidate_caches()
    try:
        import numpy
        from fastembed import TextEmbedding as TE
    except ImportError:
        return False
    np, TextEmbedding, AVAILABLE = numpy, TE, True
    return True


_import()

_model = None
_model_lock = threading.Lock()
_install_lock = threading.Lock()


# ---- installing fastembed -----------------------------------------------------------------
def _run(cmd, timeout=900):
    flags = 0x08000000 if os.name == "nt" else 0          # CREATE_NO_WINDOW: no black box on screen
    env = dict(os.environ)
    if _portable_pth():
        # A portable Python keeps everything it needs inside its own folder: don't let pip count
        # packages in the user's AppData folder as installed, which this Python may not look in.
        env["PYTHONNOUSERSITE"] = "1"
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, creationflags=flags,
                       stdin=subprocess.DEVNULL, env=env)
    return p.returncode == 0, (p.stdout + p.stderr)[-1500:]


def _python():
    """The console Python running Jarvis (pip under pythonw would still work, but keep it plain)."""
    exe = sys.executable
    if os.path.basename(exe).lower() == "pythonw.exe":
        exe = os.path.join(os.path.dirname(exe), "python.exe")
    return exe


def _portable_pth():
    """The ._pth file of a portable (embeddable) Python, which has no pip and no site-packages."""
    found = glob.glob(os.path.join(os.path.dirname(_python()), "python*._pth"))
    return found[0] if found else None


def _open_up_portable(pth, log):
    """Let a portable Python use site-packages: enable `import site` and list Lib\\site-packages."""
    home = os.path.dirname(pth)
    sp = os.path.join(home, "Lib", "site-packages")
    os.makedirs(sp, exist_ok=True)
    with open(pth, encoding="utf-8") as f:
        lines = f.read().splitlines()
    changed = False
    if "Lib\\site-packages" not in lines and sp not in lines:
        lines.insert(1, "Lib\\site-packages")
        changed = True
    for k, line in enumerate(lines):
        if line.strip() == "#import site":
            lines[k] = "import site"
            changed = True
    if not any(line.strip() == "import site" for line in lines):
        lines.append("import site")
        changed = True
    if changed:
        with open(pth, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
        log("meaning search: portable Python set up for add-ons")
    if sp not in sys.path:
        site.addsitedir(sp)       # this running server sees it too, without a restart


def _ensure_pip(log):
    ok, _ = _run([_python(), "-m", "pip", "--version"], 60)
    if ok:
        return True
    pth = _portable_pth()
    if not pth:
        log("meaning search: this Python has no pip")
        return False
    _open_up_portable(pth, log)
    os.makedirs(DATA_DIR, exist_ok=True)
    script = os.path.join(DATA_DIR, "get-pip.py")
    req = urllib.request.Request(GET_PIP, headers={"User-Agent": "Jarvis-setup"})
    with urllib.request.urlopen(req, timeout=60) as r, open(script, "wb") as out:
        out.write(r.read())
    ok, out = _run([_python(), script, "--no-warn-script-location"])
    try:
        os.remove(script)
    except OSError:
        pass
    if not ok:
        log("meaning search: couldn't install pip")
    return ok


def _attempts():
    try:
        with open(SETUP_FILE, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return {}


def _note_attempt(ok, detail=""):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(SETUP_FILE, "w", encoding="utf-8") as f:
        json.dump({"at": time.time(), "ok": ok, "detail": detail[-600:]}, f)


def ensure_installed(log=print):
    """Make fastembed importable, installing it the first time (a minute or two, in the background).
    Returns True when meaning search can run. A failed attempt waits a day before trying again."""
    if _import():
        return True
    with _install_lock:
        if _import():
            return True
        last = _attempts()
        if last and not last.get("ok") and time.time() - last.get("at", 0) < RETRY_INSTALL:
            return False
        log("meaning search: installing its add-on (fastembed), one time only")
        try:
            if not _ensure_pip(log):
                _note_attempt(False, "no pip")
                return False
            base = [_python(), "-m", "pip", "install", "--disable-pip-version-check",
                    "--no-warn-script-location", "--quiet", PACKAGE]
            ok, out = _run(base)
            if not ok and not _portable_pth():
                ok, out = _run(base + ["--user"])   # a shared Python the user can't write to
                if ok:
                    site.addsitedir(site.getusersitepackages())
            if ok and not _import():
                site.addsitedir(site.getusersitepackages())
                ok = _import()
            _note_attempt(ok, "" if ok else out)
            log("meaning search: add-on installed" if ok else "meaning search: add-on install failed")
            return ok
        except Exception as e:   # offline, blocked, disk full: keyword search carries on
            _note_attempt(False, repr(e))
            log(f"meaning search: add-on install failed ({e.__class__.__name__})")
            return False


# ---- the model ----------------------------------------------------------------------------
def model():
    """The embedding model, loaded once (first load downloads it into data/models)."""
    global _model
    if not AVAILABLE:
        return None
    with _model_lock:
        if _model is None:
            _model = TextEmbedding(MODEL_NAME, cache_dir=MODEL_DIR)
        return _model


def ready():
    """True once the model is in memory; never waits for it."""
    return _model is not None


# ---- passages and vectors -----------------------------------------------------------------
def chunks(text):
    """(offset, passage) pairs covering the text, cut at whitespace where possible."""
    text = text.strip()
    if len(text) <= CHUNK_CHARS:
        return [(0, text)] if text else []
    out, start = [], 0
    while start < len(text):
        end = min(start + CHUNK_CHARS, len(text))
        if end < len(text):
            cut = text.rfind(" ", start + CHUNK_CHARS // 2, end)
            end = cut if cut > 0 else end
        out.append((start, text[start:end]))
        if end >= len(text):
            break
        start = max(end - CHUNK_OVERLAP, start + 1)
    return out


def _passage(label, folder, body):
    return f"{label} ({folder})\n{body}"


def _key(passage):
    return hashlib.sha1(passage.encode("utf-8")).hexdigest()


def signature(notes):
    """Fingerprint of the note list's order: vectors are only valid for the list they were built from."""
    h = hashlib.sha1()
    for n in notes:
        h.update(f"{n['folder']}/{n['label']}\n".encode("utf-8"))
    return h.hexdigest()


def build(index, log=print):
    """Embed every note's passages for `index` (the note index: a list of {label, folder, text}).
    Passages whose text hasn't changed reuse their old vectors, so a rebuild after a few edits is quick."""
    if not AVAILABLE:
        return False
    if not _take_lock():
        log("meaning search: another build is embedding")
        return False
    try:
        return _build(index, log)
    finally:
        try:
            os.remove(LOCK_FILE)
        except OSError:
            pass


def _take_lock():
    os.makedirs(DATA_DIR, exist_ok=True)
    try:
        if time.time() - os.path.getmtime(LOCK_FILE) > LOCK_STALE:
            os.remove(LOCK_FILE)   # left behind by a build that was killed
    except OSError:
        pass
    try:
        os.close(os.open(LOCK_FILE, os.O_CREAT | os.O_EXCL | os.O_WRONLY))
        return True
    except FileExistsError:
        return False


def _load():
    """(meta, matrix) from the saved file, or (None, None)."""
    try:
        with np.load(VECTORS_FILE) as z:
            return json.loads(str(z["meta"])), z["vectors"]
    except (OSError, ValueError, KeyError):
        return None, None


def _build(index, log):
    old = {}
    meta, old_vecs = _load()
    if meta and meta.get("model") == MODEL_NAME and len(meta.get("chunks") or []) == len(old_vecs):
        old = {r["key"]: old_vecs[k] for k, r in enumerate(meta["chunks"])}

    rows, todo = [], []
    for i, note in enumerate(index):
        for off, body in chunks(note["text"]) or [(0, "")]:
            passage = _passage(note["label"], note["folder"], body)
            key = _key(passage)
            rows.append({"note": i, "offset": off, "key": key})
            if key not in old:
                todo.append(passage)
    todo = list(dict.fromkeys(todo))   # the same passage twice is embedded once
    sig = signature(index)
    if not todo and meta and meta.get("sig") == sig and len(rows) == len(old_vecs):
        return True                    # already up to date
    if todo:
        log(f"meaning search: {len(todo)} of {len(rows)} passages to embed")
    # A first build embeds thousands of passages, so progress is saved every few hundred: a
    # partial save (no "sig") is reused by the next build but never searched.
    for start in range(0, len(todo), CHECKPOINT):
        part = todo[start:start + CHECKPOINT]
        for p, v in zip(part, model().embed(part, batch_size=BATCH)):
            old[_key(p)] = v
        if start + CHECKPOINT < len(todo):
            os.utime(LOCK_FILE)   # still alive
            done = [{"note": -1, "offset": 0, "key": k} for k in old]
            _save(np.array(list(old.values()), dtype=np.float32), done, None)
            log(f"meaning search: {start + len(part)}/{len(todo)} embedded")
    matrix = np.array([old[r["key"]] for r in rows], dtype=np.float32)
    _save(matrix, rows, sig)
    if todo:
        log(f"meaning search: up to date ({matrix.shape[0]} passages)")
    return True


def _save(matrix, rows, sig):
    meta = json.dumps({"model": MODEL_NAME, "sig": sig, "chunks": rows}, separators=(",", ":"))
    tmp = VECTORS_FILE + ".tmp.npz"
    np.savez(tmp, vectors=matrix, meta=np.array(meta))
    os.replace(tmp, VECTORS_FILE)


class Vectors:
    """The saved passage vectors, searchable by a question's meaning."""

    def __init__(self, notes):
        self.ok = False
        if not AVAILABLE:
            return
        meta, matrix = _load()
        if meta is None:
            return
        rows = meta.get("chunks") or []
        # Vectors from a different build than the note index would point at the wrong notes.
        if meta.get("sig") != signature(notes) or len(rows) != len(matrix) or meta.get("model") != MODEL_NAME:
            return
        self.matrix = matrix
        self.note_of = np.array([r["note"] for r in rows], dtype=np.int32)
        self.offset_of = [r["offset"] for r in rows]
        self.ok = True

    def search(self, question, k=50, allowed=None):
        """[(note index, best passage offset, similarity)] for the k notes closest in meaning."""
        if not self.ok or not ready():
            return []
        q = np.array(list(model().query_embed([question]))[0], dtype=np.float32)
        sims = self.matrix @ q                          # bge vectors are unit length: dot == cosine
        if allowed is not None:                         # a project chat: only that project's notes
            sims = np.where(np.isin(self.note_of, np.fromiter(allowed, dtype=np.int32)), sims, -np.inf)
        best = {}
        for c in np.argsort(-sims)[: k * 8]:
            if not np.isfinite(sims[c]):
                break
            n = int(self.note_of[c])
            if n in best:
                continue
            best[n] = (self.offset_of[c], float(sims[c]))
            if len(best) >= k:
                break
        return [(n, off, s) for n, (off, s) in best.items()]
