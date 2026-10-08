#!/usr/bin/env python3
"""
check-version.py - the Wranglit boot-time update check.

PRIVACY NOTE (read this first)
==============================
This is the ONLY part of the Wranglit update core that reaches the network, and it
is deliberately tiny. On boot it makes one read-only HTTPS request to the
official Wranglit repository to fetch a single plain-text version string (for
example "4.0.0"). That is all it sends and all it receives. It SENDS NO DATA
ABOUT YOU: no vault contents, no file names, no identifiers, no telemetry. It is
a GET of a public version file. If you are offline, or anything goes wrong, it
stays silent and your boot continues normally (fail-silent). It compares that
remote string to your local scaffold_version (from manifest.json) and, only if a
newer version exists, prints one friendly line telling you an update is
available. It never downloads, applies, or changes anything. To turn it off,
set "update_check": {"enabled": false} in manifest.json.

This script is stdlib-only (urllib) so it runs without pip, npm, or an LLM.
"""

import json
import os
import sys
import urllib.request

# How long we are willing to wait for the version string before giving up and
# staying silent. Kept short so a slow network never delays your boot.
TIMEOUT_SECONDS = 3


def load_manifest(root):
    """Load manifest.json, or return None if it is missing/unreadable."""
    path = os.path.join(root, "manifest.json")
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, json.JSONDecodeError):
        return None


def parse_semver(text):
    """
    Turn "4.0.0" into (4, 0, 0) for comparison. Returns None if it does not
    look like a version. Tolerates stray whitespace and a leading 'v'.
    """
    if not text:
        return None
    text = text.strip().lstrip("vV").strip()
    parts = text.split(".")
    if len(parts) < 1:
        return None
    nums = []
    for p in parts[:3]:
        if not p.isdigit():
            return None
        nums.append(int(p))
    while len(nums) < 3:
        nums.append(0)
    return tuple(nums)


def fetch_remote_version(url):
    """
    Fetch the remote version string. Returns the trimmed string, or None on
    ANY problem (offline, timeout, non-200, oversized body). Fail-silent: this
    function never raises to the caller.
    """
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Wranglit-version-check"})
        with urllib.request.urlopen(req, timeout=TIMEOUT_SECONDS) as resp:
            if getattr(resp, "status", 200) != 200:
                return None
            # Read at most 64 bytes. A version string is tiny; this caps any
            # surprise payload and keeps the call cheap.
            raw = resp.read(64)
        return raw.decode("utf-8", errors="ignore").strip()
    except Exception:
        # Offline, DNS failure, timeout, TLS error, anything: stay silent.
        return None


def main():
    root = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.getcwd()

    manifest = load_manifest(root)
    if not manifest:
        return  # No manifest, nothing to compare. Stay silent.

    cfg = manifest.get("update_check", {})
    if not cfg.get("enabled", False):
        return  # Member turned the check off. Respect it. Stay silent.

    url = cfg.get("remote_version_url")
    if not url or not url.lower().startswith("https://"):
        return  # No URL, or not HTTPS. Refuse to fetch. Stay silent.

    local = parse_semver(manifest.get("scaffold_version"))
    remote_raw = fetch_remote_version(url)
    remote = parse_semver(remote_raw)

    if not local or not remote:
        return  # Could not read one side cleanly. Stay silent.

    if remote > local:
        local_s = ".".join(str(n) for n in local)
        remote_s = ".".join(str(n) for n in remote)
        print("Wranglit update available: you are on " + local_s +
              ", latest is " + remote_s + ". "
              "Run /update-scaffold (or say \"update Wranglit\") to see what changed. "
              "Nothing is downloaded or changed until you choose to.")


if __name__ == "__main__":
    main()
