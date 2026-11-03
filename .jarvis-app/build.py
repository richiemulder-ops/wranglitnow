"""Scan an Obsidian vault and write viewer/graph-data.js for the 3D knowledge galaxy.

Usage:  python build.py [path/to/vault]
Standard library only.
"""
import json
import os
import re
import sys
from collections import defaultdict
from itertools import combinations

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_VAULT = os.path.join(HERE, "..", "RTM_PKM")
OUT_FILE = os.path.join(HERE, "viewer", "graph-data.js")
INDEX_FILE = os.path.join(HERE, "data", "notes-index.json")  # server-side only, never served

EXCERPT_CHARS = 700
INDEX_CHARS = 6000           # note text kept per note for /chat answers
SKIP_DIRS = {"node_modules", "__pycache__"}  # plus any dot-folder (.obsidian, .git, .claude, .trash)
MIN_TITLE_CHARS = 4          # shorter titles are too noisy to match as mentions
MAX_MENTION_SHARE = 0.10     # titles mentioned by >10% of notes are generic words, not topics
MAX_SHARED_TARGET = 25       # a wikilink shared by more notes than this is a hub, not a relation
W_WIKILINK, W_MENTION, W_SHARED = 3, 2, 1   # link strength per direct [[link]], title mention, shared target

FRONTMATTER = re.compile(r"\A---\s*\n.*?\n---\s*\n", re.S)
WIKILINK = re.compile(r"\[\[([^\]|#^]+)(?:[#^][^\]|]*)?(?:\|[^\]]*)?\]\]")
TOKEN = re.compile(r"[a-z0-9]+")


def tokens(text):
    return TOKEN.findall(text.lower())


def clean_excerpt(text):
    text = FRONTMATTER.sub("", text)
    text = re.sub(r"```.*?```", " ", text, flags=re.S)
    text = re.sub(r"<!--.*?-->", " ", text, flags=re.S)
    text = WIKILINK.sub(lambda m: m.group(0)[2:-2].split("|")[-1], text)
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", text)
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"^\s{0,3}#{1,6}\s*", "", text, flags=re.M)
    text = re.sub(r"[*_`>|]+", "", text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n\s*\n+", "\n\n", text).strip()
    if len(text) > EXCERPT_CHARS:
        cut = text[:EXCERPT_CHARS]
        text = cut[: cut.rfind(" ")] if " " in cut[-60:] else cut
        text = text.rstrip() + "…"
    return text


def scan(vault):
    notes = []
    for root, dirs, files in os.walk(vault):
        dirs[:] = sorted(d for d in dirs if not d.startswith(".") and d not in SKIP_DIRS)
        for name in sorted(files):
            if not name.lower().endswith(".md"):
                continue
            path = os.path.join(root, name)
            rel_dir = os.path.relpath(root, vault).replace("\\", "/")
            rel_dir = "" if rel_dir == "." else rel_dir
            try:
                with open(path, encoding="utf-8", errors="replace") as f:
                    text = f.read()
            except OSError as e:
                print(f"  skip {path}: {e}", file=sys.stderr)
                continue
            notes.append({"title": name[:-3], "folder": rel_dir, "text": text})
    return notes


def build_links(notes):
    n = len(notes)
    links = defaultdict(int)  # (a, b) -> strength; the viewer draws the strongest as a clean backbone

    def add(a, b, w):
        if a != b:
            links[(min(a, b), max(a, b))] += w

    by_title = defaultdict(list)
    for i, note in enumerate(notes):
        by_title[note["title"].lower()].append(i)

    # --- 1. Title mentions: token-sequence match, indexed by each title's first token.
    title_tokens = {}
    first_index = defaultdict(list)
    for title, idxs in by_title.items():
        tt = tuple(tokens(title))
        if not tt or len(title) < MIN_TITLE_CHARS or (len(tt) == 1 and tt[0].isdigit()):
            continue
        title_tokens[title] = tt
        first_index[tt[0]].append(title)

    mentions = defaultdict(set)  # title -> notes mentioning it
    for i, note in enumerate(notes):
        toks = tokens(FRONTMATTER.sub("", note["text"]))
        for pos, tok in enumerate(toks):
            for title in first_index.get(tok, ()):
                tt = title_tokens[title]
                if toks[pos:pos + len(tt)] == list(tt):
                    mentions[title].add(i)

    limit = max(5, int(n * MAX_MENTION_SHARE))
    for title, sources in mentions.items():
        if len(sources) > limit:
            continue
        for src in sources:
            for dst in by_title[title]:
                add(src, dst, W_MENTION)

    # --- 2. Wikilinks: direct links resolve to notes; notes sharing a target are linked.
    shared = defaultdict(set)  # target -> notes that link to it
    for i, note in enumerate(notes):
        for m in WIKILINK.finditer(note["text"]):
            target = m.group(1).strip().split("/")[-1].lower()
            if target.endswith(".md"):
                target = target[:-3]
            if not target:
                continue
            shared[target].add(i)
            for dst in by_title.get(target, ()):
                add(i, dst, W_WIKILINK)
    for target, sources in shared.items():
        if 2 <= len(sources) <= MAX_SHARED_TARGET:
            for a, b in combinations(sorted(sources), 2):
                add(a, b, W_SHARED)

    return sorted(links.items())


PROJECTS_DIR = "copilot/projects"   # one folder per project (Obsidian Copilot's fixed path)
PROJECTS_INDEX = "Projects.md"      # vault-root index with a "| Project | What it covers | Deliverables |" table
PROJECT_QUALIFIERS = re.compile(r"^(fy\d{2,4}|annual)$")


def project_key(name):
    """Core name used to find a project across the vault: 'Allied Pinnacle - Scope 3' -> allied pinnacle,
    'Autoleague FY27' -> autoleague, 'Siecap Annual' -> siecap."""
    toks = tokens(name.split(" - ")[0])
    while len(toks) > 1 and PROJECT_QUALIFIERS.match(toks[-1]):
        toks.pop()
    return toks


def build_projects(vault, notes):
    names = []
    proj_root = os.path.join(vault, *PROJECTS_DIR.split("/"))
    if os.path.isdir(proj_root):
        names = sorted(d for d in os.listdir(proj_root)
                       if not d.startswith(".") and os.path.isdir(os.path.join(proj_root, d)))

    # Descriptions and deliverable counts from the Projects.md table, in its order.
    meta = {}
    try:
        with open(os.path.join(vault, PROJECTS_INDEX), encoding="utf-8") as f:
            for line in f:
                cells = [c.strip() for c in line.strip().strip("|").split("|")]
                if len(cells) >= 2 and line.lstrip().startswith("|") and cells[0] not in ("Project", "") \
                        and not set(cells[0]) <= set("-: "):
                    meta[cells[0]] = {"description": cells[1],
                                      "deliverables": int(cells[2]) if len(cells) > 2 and cells[2].isdigit() else None}
    except OSError:
        pass
    order = list(meta) + [n for n in names if n not in meta]

    # Token views of every note for phrase matching ("auto league" and "autoleague" both match).
    views = []
    for note in notes:
        toks = tokens(note["title"] + " " + FRONTMATTER.sub("", note["text"]))
        views.append((" " + " ".join(toks) + " ", set(toks) | {a + b for a, b in zip(toks, toks[1:])}))

    projects = []
    for name in order:
        key = project_key(name)
        if not key:
            continue
        phrase, joined = " " + " ".join(key) + " ", "".join(key)
        folder = f"{PROJECTS_DIR}/{name}"
        # Score how much each note is *about* the project: its own folder first, then notes
        # named after it, then by how often the text mentions it.
        scored = []
        for i, (note, (text, words)) in enumerate(zip(notes, views)):
            own = note["folder"] == folder or note["folder"].startswith(folder + "/")
            hits = text.count(phrase) + (joined in words and len(key) == 1)
            if own or hits:
                named = joined in "".join(tokens(note["title"]))
                scored.append((-(2 * own + named), -hits, i))
        related = [i for *_, i in sorted(scored)]
        projects.append({
            "name": name,
            "description": meta.get(name, {}).get("description", ""),
            "deliverables": meta.get(name, {}).get("deliverables"),
            "nodes": related,  # node ids (== indexes) of every note about this project, most relevant first
        })
    return projects


TEAM_DIR = "Team"                   # one folder per agent: "Larry - Orchestrator", "Penn - Journal Writer", ...
AGENT_DEFS_DIR = ".claude/agents"   # <name>.md with a frontmatter description


def build_agents(vault, notes):
    team_root = os.path.join(vault, TEAM_DIR)
    if not os.path.isdir(team_root):
        return []
    agents = []
    for entry in sorted(os.listdir(team_root)):
        if " - " not in entry or not os.path.isdir(os.path.join(team_root, entry)):
            continue
        name, role = (s.strip() for s in entry.split(" - ", 1))
        description = ""
        try:
            with open(os.path.join(vault, *AGENT_DEFS_DIR.split("/"), name.lower() + ".md"), encoding="utf-8") as f:
                m = re.search(r"^description:\s*(.+)$", f.read(), re.M)
                if m:
                    description = m.group(1).strip().strip('"')
        except OSError:
            pass
        # Names like Ledger or Tally are also words, so only the capitalised name counts as a mention.
        mention = re.compile(r"\b" + re.escape(name) + r"\b")
        folder = f"{TEAM_DIR}/{entry}"
        scored = []
        for i, note in enumerate(notes):
            own = note["folder"] == folder or note["folder"].startswith(folder + "/")
            hits = len(mention.findall(note["title"] + " " + note["text"]))
            if own or hits:
                scored.append((-(2 * own + bool(mention.search(note["title"]))), -hits, i))
        agents.append({"name": name, "role": role, "description": description,
                       "nodes": [i for *_, i in sorted(scored)]})
    return agents


def main():
    vault = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else DEFAULT_VAULT)
    if not os.path.isdir(vault):
        sys.exit(f"Vault not found: {vault}")
    print(f"Scanning {vault}")
    notes = scan(vault)
    print(f"  {len(notes)} notes")
    links = build_links(notes)
    print(f"  {len(links)} links")

    nodes = [
        {
            "id": i,  # id == index in nodes[]; later features look nodes up by index
            "label": note["title"],
            "group": note["folder"].split("/")[0] if note["folder"] else "(root)",
            "folder": note["folder"] or "(root)",
            "excerpt": clean_excerpt(note["text"]),
        }
        for i, note in enumerate(notes)
    ]
    projects = build_projects(vault, notes)
    print(f"  {len(projects)} projects: " + ", ".join(f"{p['name']} ({len(p['nodes'])})" for p in projects))
    agents = build_agents(vault, notes)
    print(f"  {len(agents)} agents: " + ", ".join(f"{a['name']} ({len(a['nodes'])})" for a in agents))
    data = {"nodes": nodes, "links": [{"source": a, "target": b, "w": w} for (a, b), w in links],
            "projects": projects, "agents": agents}

    os.makedirs(os.path.dirname(OUT_FILE), exist_ok=True)
    with open(OUT_FILE, "w", encoding="utf-8") as f:
        f.write("// Generated by build.py. Do not edit by hand.\n")
        f.write("const GRAPH = ")
        json.dump(data, f, ensure_ascii=False, separators=(",", ":"))
        f.write(";\n")
    print(f"Wrote {OUT_FILE} ({os.path.getsize(OUT_FILE) / 1e6:.1f} MB)")

    # Full-ish note text for server.py's /chat, in the same order (index == node id).
    index = [
        {"label": note["title"], "folder": note["folder"] or "(root)",
         "text": FRONTMATTER.sub("", note["text"]).strip()[:INDEX_CHARS]}
        for note in notes
    ]
    os.makedirs(os.path.dirname(INDEX_FILE), exist_ok=True)
    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, separators=(",", ":"))
    print(f"Wrote {INDEX_FILE} ({os.path.getsize(INDEX_FILE) / 1e6:.1f} MB)")


if __name__ == "__main__":
    main()
