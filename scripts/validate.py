#!/usr/bin/env python3
"""Validate the Cadasto marketplace manifests and keep the Cursor twin in sync.

Checks, in order:
  1. `.claude-plugin/marketplace.json` — required fields, naming rules, and the
     conventions this marketplace commits to (pinned GitHub sources, full metadata).
  2. `.cursor-plugin/marketplace.json` — must equal the Claude manifest with the
     `$schema` key dropped. Generated for field parity, not as Cursor's native
     multi-plugin schema (that schema expects in-repo plugin paths).
  3. `README.md` — the "Available Plugins" table must list exactly the plugins
     in the manifest, in the same order (names only; descriptions may be shortened).
  4. `CHANGELOG.md` — the catalog version in `metadata.version` must have a
     matching dated released section, so a bump cannot ship undocumented.

Usage:
  python3 scripts/validate.py           # verify; non-zero exit on any error
  python3 scripts/validate.py --fix     # regenerate the Cursor twin, then verify
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CLAUDE_MANIFEST = ROOT / ".claude-plugin" / "marketplace.json"
CURSOR_MANIFEST = ROOT / ".cursor-plugin" / "marketplace.json"
README = ROOT / "README.md"
CHANGELOG = ROOT / "CHANGELOG.md"

# Claude Code ignores `$schema` at load. The twin drops it so the two files
# stay a mechanical projection; Cursor's own marketplace schema is different.
CURSOR_DROPPED_KEYS = ("$schema",)
SCHEMA_URL = "https://json.schemastore.org/claude-code-marketplace.json"

MARKETPLACE_NAME_RE = re.compile(r"^[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$")
PLUGIN_NAME_RE = re.compile(r"^[a-z0-9](?:[a-z0-9.-]*[a-z0-9])?$")
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")
# Release tags across the Cadasto plugin repos are `vX.Y.Z`.
REF_RE = re.compile(r"^v\d+\.\d+\.\d+$")

# Fields every entry carries, so `/plugin` can present and filter the catalog.
REQUIRED_PLUGIN_FIELDS = (
    "name",
    "displayName",
    "description",
    "version",
    "author",
    "homepage",
    "license",
    "category",
    "keywords",
    "source",
)

errors = []


def err(msg):
    errors.append(msg)


def load(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        err(f"{path.relative_to(ROOT)}: missing")
    except json.JSONDecodeError as e:
        err(f"{path.relative_to(ROOT)}: invalid JSON: {e}")
    return None


def read_text(path):
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        err(f"{path.relative_to(ROOT)}: missing")
        return None


def cursor_twin(claude):
    return {k: v for k, v in claude.items() if k not in CURSOR_DROPPED_KEYS}


def validate_claude(m):
    for field in ("$schema", "name", "description", "owner", "plugins"):
        if field not in m:
            err(f"marketplace.json: missing '{field}'")
    if m.get("$schema") and m["$schema"] != SCHEMA_URL:
        err(f"marketplace.json: $schema must be '{SCHEMA_URL}'")
    name = m.get("name", "")
    if name and not MARKETPLACE_NAME_RE.match(name):
        err(f"marketplace.json: name '{name}' is not kebab-case")
    # House rule: only `metadata.version` (the catalog release counter).
    # Claude also accepts `version` and `description` under `metadata`.
    for key in m.get("metadata", {}):
        if key != "version":
            err(f"marketplace.json: move 'metadata.{key}' to the top level")

    owner = m.get("owner") or {}
    if not isinstance(owner, dict):
        err("marketplace.json: owner must be an object")
        owner = {}
    for field in ("name", "email", "url"):
        if not owner.get(field):
            err(f"marketplace.json: owner missing '{field}'")

    plugins = m.get("plugins")
    if not isinstance(plugins, list):
        err("marketplace.json: plugins must be an array")
        return

    seen = set()
    for i, p in enumerate(plugins):
        if not isinstance(p, dict):
            err(f"plugins[{i}]: entry must be an object")
            continue
        label = f"plugins[{i}]" + (f" ({p['name']})" if "name" in p else "")
        for field in REQUIRED_PLUGIN_FIELDS:
            if field not in p:
                err(f"{label}: missing '{field}'")

        pname = p.get("name", "")
        if pname and not PLUGIN_NAME_RE.match(pname):
            err(f"{label}: name '{pname}' is not a valid plugin name")
        if pname in seen:
            err(f"{label}: duplicate plugin name '{pname}'")
        seen.add(pname)

        version = p.get("version", "")
        if "version" in p and not SEMVER_RE.match(version or ""):
            err(f"{label}: version '{version}' is not semver")

        keywords = p.get("keywords")
        if "keywords" in p and (not isinstance(keywords, list) or keywords == []):
            err(f"{label}: keywords must be a non-empty array")

        author = p.get("author")
        if "author" in p:
            if not isinstance(author, dict):
                err(f"{label}: author must be an object")
            else:
                for field in ("name", "url"):
                    if not author.get(field):
                        err(f"{label}: author missing '{field}'")

        src = p.get("source")
        if not isinstance(src, dict):
            err(f"{label}: source must be an object pinned to a release tag")
            continue
        if src.get("source") != "github":
            err(f"{label}: source.source must be 'github'")
            continue
        repo = src.get("repo", "")
        if not re.match(r"^[\w.-]+/[\w.-]+$", repo):
            err(f"{label}: source.repo '{repo}' is not 'owner/name'")
        # Unpinned sources ship every push to the default branch straight to users.
        ref = src.get("ref", "")
        if not ref:
            err(f"{label}: source.ref missing — pin the entry to a release tag")
        elif not REF_RE.match(ref):
            err(f"{label}: source.ref '{ref}' is not a vX.Y.Z release tag")
        elif version and ref != f"v{version}":
            err(f"{label}: source.ref '{ref}' does not match version '{version}'")


def validate_cursor(claude):
    actual = load(CURSOR_MANIFEST)
    if actual is None:
        return
    if actual != cursor_twin(claude):
        err(
            ".cursor-plugin/marketplace.json is out of sync with "
            ".claude-plugin/marketplace.json — run: python3 scripts/validate.py --fix"
        )


def validate_readme(claude):
    text = read_text(README)
    if text is None:
        return
    section = re.search(r"^## Available Plugins$(.*?)^## ", text, re.S | re.M)
    if not section:
        err("README.md: no 'Available Plugins' section")
        return
    rows = re.findall(r"^\|\s*\[`?([^\]`]+)`?\]", section.group(1), re.M)
    expected = [p.get("name") for p in claude.get("plugins", [])]
    if rows != expected:
        err(f"README.md: plugin table lists {rows}, manifest has {expected}")


def validate_changelog(claude):
    version = claude.get("metadata", {}).get("version")
    if not version:
        err("marketplace.json: metadata.version missing — the catalog's release counter")
        return
    text = read_text(CHANGELOG)
    if text is None:
        return
    if not re.search(rf"^## \[{re.escape(version)}\] - \d{{4}}-\d{{2}}-\d{{2}}$", text, re.M):
        err(f"CHANGELOG.md: no dated section for the current version [{version}]")


def main():
    fix = "--fix" in sys.argv[1:]

    claude = load(CLAUDE_MANIFEST)
    if claude is None:
        print("\n".join(f"  ✘ {e}" for e in errors))
        return 1

    if fix:
        CURSOR_MANIFEST.parent.mkdir(exist_ok=True)
        CURSOR_MANIFEST.write_text(
            json.dumps(cursor_twin(claude), indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        print(f"wrote {CURSOR_MANIFEST.relative_to(ROOT)}")

    validate_claude(claude)
    validate_cursor(claude)
    validate_readme(claude)
    validate_changelog(claude)

    if errors:
        print(f"✘ {len(errors)} problem(s):")
        print("\n".join(f"  ✘ {e}" for e in errors))
        return 1

    count = len(claude.get("plugins", []))
    print(f"✔ marketplace '{claude['name']}' valid — {count} plugin(s), Cursor twin in sync")
    return 0


if __name__ == "__main__":
    sys.exit(main())
