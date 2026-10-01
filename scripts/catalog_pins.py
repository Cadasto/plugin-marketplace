#!/usr/bin/env python3
"""Keep the site's plugin pins and the install include aligned with the catalog.

Two outputs, both under ``.fetched/``:

* ``catalog.md`` is the plugins table. Descriptions and release tags are read
  from ``.claude-plugin/marketplace.json``, so a repin cannot leave the table
  behind.
* ``catalog-install.md`` is ``docs/install.md`` with its title removed and its
  in-repo links rewritten for the site. The install page includes it, so the
  GitHub doc stays the only copy of those steps.

The script also fails when ``sources.json`` does not list each plugin's
``source.repo`` and ``source.ref`` exactly. Run it before ``sync_sources.py``.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / ".claude-plugin" / "marketplace.json"
SOURCES = ROOT / "sources.json"
INSTALL = ROOT / "docs" / "install.md"
OUT_DIR = ROOT / ".fetched"

# A relative link target. Anchors, absolute URLs, and site-root paths stay out.
RELATIVE_LINK = re.compile(r"\]\((?!https?:|mailto:|#|/)([^)\s]+)")
# Produced by INSTALL_REWRITES. MkDocs resolves it from pages/install.md.
ALLOWED_RELATIVE = {"plugins/index.md"}

# Rewrites that are correct on the site and would be wrong if left as GitHub
# paths. Anything else relative still fails the scan below, so a new link in
# docs/install.md has to be added here on purpose.
INSTALL_REWRITES = (
    (
        "[README plugin table](../README.md#available-plugins)",
        "[plugin list](plugins/index.md)",
    ),
    (
        "[README.md](../README.md)",
        "[README.md](https://github.com/Cadasto/plugin-marketplace/blob/main/README.md)",
    ),
    (
        "](versioning.md)",
        "](https://github.com/Cadasto/plugin-marketplace/blob/main/docs/versioning.md)",
    ),
)


def fail(message: str) -> None:
    print(f"catalog: {message}", file=sys.stderr)
    raise SystemExit(1)


def drop_leading_heading(text: str) -> str:
    lines = text.splitlines(keepends=True)
    for i, line in enumerate(lines):
        if line.strip():
            if line.lstrip().startswith("#"):
                return "".join(lines[i + 1 :]).lstrip("\n")
            break
    return text


def load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        fail(f"cannot read {path.relative_to(ROOT)}: {error}")
        raise AssertionError("unreachable")


def check_sources(manifest: dict, config: dict) -> list[dict]:
    plugins = manifest.get("plugins")
    if not isinstance(plugins, list) or not plugins:
        fail("marketplace.json has no plugins")

    sources = config.get("sources")
    if not isinstance(sources, list):
        fail('sources.json "sources" must be an array')

    by_name = {}
    for source in sources:
        name = source.get("name")
        if not name or name in by_name:
            fail(f"sources.json has a missing or duplicate name: {source!r}")
        by_name[name] = source

    expected = []
    for plugin in plugins:
        name = plugin["name"]
        src = plugin["source"]
        source = by_name.pop(name, None)
        if source is None:
            fail(
                f"{name} is in the marketplace but sources.json has no entry. "
                f"Add repo {src['repo']} ref {src['ref']} path README.md."
            )
        if source.get("repo") != src["repo"] or source.get("ref") != src["ref"]:
            fail(
                f"{name}: sources.json has {source.get('repo')}@{source.get('ref')}, "
                f"marketplace.json has {src['repo']}@{src['ref']}."
            )
        if source.get("path") != "README.md":
            fail(f"{name}: sources.json path must be README.md.")
        if not source.get("drop_first_heading"):
            fail(f"{name}: set drop_first_heading so the site supplies the only H1.")
        if source.get("heading_shift") != 1:
            fail(f"{name}: set heading_shift to 1 so the README nests under the page H1.")
        expected.append(plugin)

    if by_name:
        extra = ", ".join(sorted(by_name))
        fail(f"sources.json lists plugins that are not in the marketplace: {extra}")
    return expected


def write_catalog(plugins: list[dict]) -> None:
    rows = [
        "| Plugin | Pinned release | Description |",
        "|---|---|---|",
    ]
    for plugin in plugins:
        name = plugin["name"]
        ref = plugin["source"]["ref"]
        description = " ".join(plugin["description"].split()).replace("|", "\\|")
        rows.append(
            f"| [{name}]({name}.md) | `{ref}` | {description} |"
        )
    body = "\n".join(rows) + "\n"
    dest = OUT_DIR / "catalog.md"
    dest.write_text(
        "<!-- Generated from .claude-plugin/marketplace.json by "
        "scripts/catalog_pins.py. Do not edit. -->\n\n" + body,
        encoding="utf-8",
    )
    print(f"  ✓ {dest.relative_to(ROOT)}")


def write_install() -> None:
    try:
        text = INSTALL.read_text(encoding="utf-8")
    except OSError as error:
        fail(f"cannot read docs/install.md: {error}")
    text = drop_leading_heading(text)
    for old, new in INSTALL_REWRITES:
        if old not in text:
            fail(
                "docs/install.md no longer contains the link "
                f"{old!r}, so the site rewrite does not apply. "
                "Update INSTALL_REWRITES in scripts/catalog_pins.py."
            )
        text = text.replace(old, new)
    leftover = sorted(set(RELATIVE_LINK.findall(text)) - ALLOWED_RELATIVE)
    if leftover:
        fail(
            "docs/install.md still has relative links the site cannot resolve: "
            + ", ".join(leftover)
        )
    dest = OUT_DIR / "catalog-install.md"
    dest.write_text(
        "<!-- Generated from docs/install.md by scripts/catalog_pins.py. "
        "Edit that file, not this one. -->\n\n" + text,
        encoding="utf-8",
    )
    print(f"  ✓ {dest.relative_to(ROOT)}")


def main() -> int:
    manifest = load_json(MANIFEST)
    config = load_json(SOURCES)
    plugins = check_sources(manifest, config)
    OUT_DIR.mkdir(exist_ok=True)
    write_catalog(plugins)
    write_install()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
