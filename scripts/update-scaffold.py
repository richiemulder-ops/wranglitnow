#!/usr/bin/env python3
"""
update-scaffold.py - the Wranglit scaffold updater.

WHAT THIS IS, IN PLAIN ENGLISH
==============================
This script updates the "framework" part of your Wranglit folder (the parts we
ship and maintain: SOPs, Workstreams, Guidelines, templates, agent contracts,
the changelog, and so on) WITHOUT EVER touching "your" part (your notes, your
journal, your team's memory, your installed Expansions, your secrets, your
databases).

It can do this safely because the boundary between "ours" and "yours" is
written down as data in manifest.json:
  - framework_paths  = the files we MAY overwrite (ours, upgradable)
  - user_state_paths = the files we will NEVER touch (yours, sacred)

This script only ever writes inside framework_paths, and it refuses to write
anything that matches user_state_paths even if asked to.

HOW IT WORKS
============
1. It reads your LOCAL manifest.json (where you are now).
2. It reads a TARGET manifest.json (the new version you are updating to). You
   point at it with --target /path/to/new/manifest.json. (Fetching the new
   version from the internet is a separate concern; this script works on a
   target you already have on disk, so it is fully OFFLINE-SAFE.)
3. It compares the two and builds a plain-English plan: how many files are
   new, how many changed, and confirms that ZERO of your files are touched.
4. By default it only PRINTS the plan and changes nothing (a dry run).
5. It applies the changes only when you pass --apply.
6. Before it overwrites any framework file that YOU have locally modified, it
   first copies your version into .mypka/backups/<timestamp>/ so your edit is
   never silently lost.

WHAT IT WILL NOT DO
===================
- It will NOT touch anything under user_state_paths (PKM/, your journal,
  Team Inbox/, tasks/, session-logs/, Expansions/, .env, the databases).
- It will NOT update Expansion code (the cockpit and friends). Expansions are
  versioned on their own expansion.yaml and have their own updater. If your
  cockpit is behind, this script just tells you to run the cockpit updater.
- It will NOT reach out to the internet. (The boot-time version check is a
  different, tiny script: scripts/check-version.py.)
- It will NOT write a single byte in dry-run mode (the default).

This file is deliberately written with stdlib only (no pip, no npm) so it runs
on any machine with python3, with or without an LLM session.
"""

import argparse
import datetime
import fnmatch
import hashlib
import json
import os
import shutil
import sys

# ---------------------------------------------------------------------------
# Small helpers
# ---------------------------------------------------------------------------

def read_json(path):
    """Load a JSON file, or exit with a clear message if it is missing/bad."""
    if not os.path.isfile(path):
        fail("Could not find a manifest at: " + path)
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return json.load(fh)
    except json.JSONDecodeError as exc:
        fail("That manifest is not valid JSON (" + path + "): " + str(exc))


def fail(message):
    """Print an error and stop. We fail CLOSED: when in doubt, do nothing."""
    print("STOP: " + message, file=sys.stderr)
    sys.exit(1)


def sha256_of(path):
    """Return the sha256 of a file, or None if the file does not exist."""
    if not os.path.isfile(path):
        return None
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def matches_any(rel_path, globs):
    """
    True if rel_path matches any glob in the list.

    We normalise to forward slashes (manifest globs are forward-slash) and we
    treat a trailing /** as "this directory and everything under it". We also
    treat a bare directory glob as covering its contents. This is intentionally
    conservative: it is better to mistakenly PROTECT a file than to mistakenly
    overwrite one.
    """
    p = rel_path.replace(os.sep, "/")
    for g in globs:
        g = g.replace(os.sep, "/")
        if fnmatch.fnmatch(p, g):
            return True
        # Treat "dir/**" as also matching "dir/anything/deep".
        if g.endswith("/**"):
            base = g[:-3]
            if p == base or p.startswith(base + "/"):
                return True
        # Treat "dir/" as covering everything underneath it.
        if g.endswith("/") and p.startswith(g):
            return True
    return False


# ---------------------------------------------------------------------------
# Core logic
# ---------------------------------------------------------------------------

def load_manifests(root, target_path):
    """Read the local and target manifests and do basic sanity checks."""
    local_path = os.path.join(root, "manifest.json")
    local = read_json(local_path)
    target = read_json(target_path)

    if "framework_paths" not in target or "user_state_paths" not in target:
        fail("The target manifest is missing framework_paths/user_state_paths. "
             "Refusing to proceed (fail-closed).")

    return local, target


def expansion_notice(local, target):
    """
    Compare declared Expansion versions and, if any installed Expansion is
    behind, print a notice telling the member to run that Expansion's own
    updater. The scaffold updater NEVER updates Expansion code itself.
    """
    def index_expansions(manifest):
        out = {}
        for item in manifest.get("expansions", {}).get("items", []):
            out[item.get("slug")] = item
        return out

    local_ex = index_expansions(local)
    target_ex = index_expansions(target)

    behind = []
    for slug, t in target_ex.items():
        l = local_ex.get(slug)
        if not l:
            continue
        if str(l.get("expansion_yaml_version")) != str(t.get("expansion_yaml_version")):
            behind.append((slug, l.get("expansion_yaml_version"),
                           t.get("expansion_yaml_version"), t.get("updater")))

    if behind:
        print("")
        print("Note about your Expansions (these update separately):")
        for slug, have, want, updater in behind:
            line = ("  - " + str(slug) + " is at " + str(have) +
                    "; latest is " + str(want) + ".")
            if slug == "mypka-cockpit":
                line += " Your cockpit is behind. Run the cockpit updater separately"
                if updater:
                    line += " (see " + updater + ")"
                line += "."
            else:
                line += " Update it via its own Expansion update path."
            print(line)
        print("  The scaffold updater does not change Expansion code.")


def build_plan(root, target, target_manifest_path):
    """
    Build the list of file operations from the target's `changes` block.

    Each entry becomes one of:
      - "new"        : file does not exist locally; will be created.
      - "update"     : file exists locally and is UNMODIFIED from our shipped
                       version; will be overwritten cleanly.
      - "update+bak" : file exists locally and YOU have modified it; we will
                       back it up first, then overwrite.
      - "skip-same"  : local file already matches the target; nothing to do.

    Any path that is NOT inside framework_paths, or that IS inside
    user_state_paths, is refused outright (fail-closed). Source files for the
    target version are expected to sit next to the target manifest.json.
    """
    fw_globs = target["framework_paths"]["globs"]
    user_globs = target["user_state_paths"]["globs"]
    target_dir = os.path.dirname(os.path.abspath(target_manifest_path))

    plan = []
    refused = []

    for entry in target.get("changes", {}).get("paths", []):
        rel = entry["path"]

        # --- Safety gate 1: never write user-state, no matter what. ----------
        if matches_any(rel, user_globs):
            refused.append((rel, "matches a sacred user_state path"))
            continue

        # --- Safety gate 2: only write inside the framework allow-list. ------
        if not matches_any(rel, fw_globs):
            refused.append((rel, "is not on the framework_paths allow-list"))
            continue

        # --- Safety gate 3: never escape the scaffold root. ------------------
        local_abs = os.path.normpath(os.path.join(root, rel))
        if not local_abs.startswith(os.path.normpath(root) + os.sep) \
                and local_abs != os.path.normpath(root):
            refused.append((rel, "would write outside the scaffold root"))
            continue

        # The new version of this file ships alongside the target manifest.
        src_abs = os.path.normpath(os.path.join(target_dir, rel))

        local_hash = sha256_of(local_abs)
        src_hash = sha256_of(src_abs)

        if src_hash is None:
            # The target says this path changed but the new file is not in the
            # update bundle. Skip it rather than guess. (Version files like
            # VERSION are tiny and handled even without a separate source copy
            # by the dry-run plan; an --apply with a real bundle includes them.)
            plan.append((rel, "skip-missing-source", local_abs, src_abs))
            continue

        if local_hash is None:
            plan.append((rel, "new", local_abs, src_abs))
        elif local_hash == src_hash:
            plan.append((rel, "skip-same", local_abs, src_abs))
        else:
            # The file differs. Did WE change it (new shipped version) or did
            # the member change it locally? We cannot know the member's edit
            # intent from hashes alone, so we treat ANY local difference as
            # "worth backing up" before overwrite. This is the never-silent
            # -overwrite-a-member-edit rule.
            plan.append((rel, "update+bak", local_abs, src_abs))

    return plan, refused


def print_plan(plan, refused, target):
    """Print the plain-English plan. No writes happen here."""
    new = [p for p in plan if p[1] == "new"]
    upd = [p for p in plan if p[1] in ("update", "update+bak")]
    same = [p for p in plan if p[1] == "skip-same"]
    missing = [p for p in plan if p[1] == "skip-missing-source"]

    ver_from = target.get("from", "?")
    ver_to = target.get("scaffold_version", "?")

    print("Wranglit scaffold update plan: " + str(ver_from) + " -> " + str(ver_to))
    print("")
    print("  " + str(len(new)) + " new file(s)")
    print("  " + str(len(upd)) + " changed file(s)")
    print("  " + str(len(same)) + " already up to date")
    print("  0 of your files touched (your PKM, journal, Expansions, secrets, "
          "and databases are never written by this updater)")

    if new:
        print("")
        print("Would add:")
        for rel, _, _, _ in new:
            print("  + " + rel)
    if upd:
        print("")
        print("Would update:")
        for rel, kind, _, _ in upd:
            tag = "  ~ " + rel
            if kind == "update+bak":
                tag += "   (your local copy differs; it will be backed up first)"
            print(tag)
    if missing:
        print("")
        print("Listed as changed but no new copy was found in this update bundle "
              "(skipped, nothing done):")
        for rel, _, _, _ in missing:
            print("  ? " + rel)
    if refused:
        print("")
        print("Refused for safety (not written under any circumstance):")
        for rel, why in refused:
            print("  ! " + rel + "  -> " + why)


def apply_plan(root, plan):
    """
    Apply the plan. Only called when --apply is passed. Backs up any locally
    modified framework file before overwriting it.
    """
    stamp = datetime.datetime.now().strftime("%Y-%m-%d-%H%M%S")
    backup_dir = os.path.join(root, ".mypka", "backups", stamp)
    log_path = os.path.join(root, ".mypka", "update-log.txt")

    # Create the .mypka/ control folder on first run.
    os.makedirs(os.path.join(root, ".mypka"), exist_ok=True)

    applied = []
    backed_up = []

    for rel, kind, local_abs, src_abs in plan:
        if kind in ("skip-same", "skip-missing-source"):
            continue

        if kind == "update+bak":
            # Back up the member's current copy before we overwrite it.
            os.makedirs(backup_dir, exist_ok=True)
            dest = os.path.join(backup_dir, rel)
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            shutil.copy2(local_abs, dest)
            backed_up.append(rel)

        # Ensure the destination directory exists, then copy the new file in.
        os.makedirs(os.path.dirname(local_abs), exist_ok=True)
        shutil.copy2(src_abs, local_abs)
        applied.append((rel, kind))

    # Write a copy of the active manifest into the control folder.
    try:
        shutil.copy2(os.path.join(root, "manifest.json"),
                     os.path.join(root, ".mypka", "active-manifest.json"))
    except OSError:
        pass

    # Append to the update log so there is an auditable record.
    with open(log_path, "a", encoding="utf-8") as log:
        log.write("[" + stamp + "] applied " + str(len(applied)) +
                  " file(s); backed up " + str(len(backed_up)) + " file(s)")
        if backed_up:
            log.write(" to .mypka/backups/" + stamp + "/")
        log.write("\n")

    print("")
    print("Applied " + str(len(applied)) + " file(s).")
    if backed_up:
        print("Backed up " + str(len(backed_up)) +
              " of your locally modified file(s) to .mypka/backups/" + stamp + "/")
    print("Logged to .mypka/update-log.txt")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Safely update the framework part of your Wranglit scaffold. "
                    "Dry-run by default. Never touches your own files.")
    parser.add_argument(
        "--root", default=".",
        help="Path to your Wranglit scaffold root (the folder with manifest.json). "
             "Defaults to the current directory.")
    parser.add_argument(
        "--target", required=True,
        help="Path to the TARGET manifest.json (the new version you are "
             "updating to). The new files are expected to sit next to it.")
    parser.add_argument(
        "--apply", action="store_true",
        help="Actually apply the update. Without this flag, the script only "
             "prints the plan and changes nothing (dry run).")
    args = parser.parse_args()

    root = os.path.abspath(args.root)
    if not os.path.isfile(os.path.join(root, "manifest.json")):
        fail("No manifest.json at " + root +
             ". Point --root at your Wranglit scaffold root.")

    local, target = load_manifests(root, args.target)
    plan, refused = build_plan(root, target, args.target)

    print_plan(plan, refused, target)
    expansion_notice(local, target)

    if not args.apply:
        print("")
        print("This was a dry run. Nothing was changed.")
        print("Re-run with --apply to perform the update.")
        return

    # A target manifest that names a sacred path is a sign of a bad/hostile
    # bundle. We already filtered those into `refused`; if any exist, stop.
    if refused:
        fail("The target manifest tried to write " + str(len(refused)) +
             " path(s) it is not allowed to write. Refusing to apply "
             "(fail-closed). Review the 'Refused for safety' list above.")

    apply_plan(root, plan)


if __name__ == "__main__":
    main()
