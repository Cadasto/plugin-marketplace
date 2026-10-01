#!/usr/bin/env python3
"""Assert the built site is publishable.

MkDocs strict mode cannot see a missing stylesheet link, a landing template
that did not apply, or a plugin page that forgot its fetched README. This is
the check ``make docs-check`` runs after the build.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
MKDOCS = ROOT / "mkdocs.yml"
SOURCES = ROOT / "sources.json"
MANIFEST = ROOT / ".claude-plugin" / "marketplace.json"
INSTALL = ROOT / "docs" / "install.md"
QUICK_START = ROOT / "pages" / "quick-start.md"

ADD_COMMAND = "/plugin marketplace add Cadasto/plugin-marketplace"
FONT_DIR = SITE / "assets" / "external" / "fonts.googleapis.com"
WOFF_DIR = SITE / "assets" / "external" / "fonts.gstatic.com"

NAV_LINE = re.compile(r"^\s*-\s+.*:\s*([A-Za-z0-9_./-]+)\.md\s*$")
SITE_URL_LINE = re.compile(r"^site_url:\s*(\S+)\s*$")


def fail(message: str) -> None:
    print(f"docs-check: {message}", file=sys.stderr)
    raise SystemExit(1)


def read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError as error:
        fail(f"cannot read {path.relative_to(ROOT)}: {error}")
        raise AssertionError("unreachable")


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def nav_slugs(text: str) -> list[str]:
    slugs = []
    in_nav = False
    for line in text.splitlines():
        if not in_nav:
            if line.startswith("nav:"):
                in_nav = True
            continue
        if line and not line.startswith((" ", "\t", "#")):
            break
        match = NAV_LINE.match(line)
        if match:
            slugs.append(match.group(1))
    return slugs


def page_url(site_url: str, slug: str) -> str:
    if slug == "index":
        return site_url
    if slug.endswith("/index"):
        return site_url + slug[: -len("index")]
    return site_url + slug + "/"


def main() -> int:
    mkdocs = read(MKDOCS)
    site_urls = []
    for line in mkdocs.splitlines():
        match = SITE_URL_LINE.match(line)
        if match:
            site_urls.append(match.group(1))
    require(len(site_urls) == 1, "mkdocs.yml must set site_url once")
    site_url = site_urls[0]
    require(site_url.endswith("/"), "site_url must end with a slash")

    slugs = nav_slugs(mkdocs)
    require(slugs, "no page slugs parsed from the mkdocs.yml nav")

    index = read(SITE / "index.html")
    install = read(SITE / "install" / "index.html")
    quick = read(SITE / "quick-start" / "index.html")
    choose = read(SITE / "choose" / "index.html")
    contact = read(SITE / "contact" / "index.html")
    contributing = read(SITE / "contributing" / "index.html")
    tokens = read(SITE / "stylesheets" / "tokens.css")

    require((SITE / "index.html").stat().st_size > 0, "no index.html")
    for name in ("tokens.css", "material.css", "landing.css"):
        path = SITE / "stylesheets" / name
        require(path.is_file() and path.stat().st_size > 0, f"{name} was not emitted")
        require(f"stylesheets/{name}" in install, f"{name} is not linked from the install page")
    require((SITE / "assets" / "cadasto-mark.png").is_file(), "company mark was not emitted")
    require((SITE / "assets" / "logo.svg").is_file(), "logo was not emitted")
    require("home-nav" in index, "landing template did not apply")
    require('markdown="1"' not in index, 'literal markdown="1" reached the landing page')
    require("[data-md-color-scheme=\"slate\"]" in tokens, "tokens.css has no dark scheme")
    require("[data-md-color-scheme=\"default\"]" in tokens, "tokens.css has no light scheme")
    require('data-md-component="palette"' in install, "palette toggle is missing from docs pages")
    for scheme in ("slate", "default"):
        require(
            f'data-md-color-scheme="{scheme}"' in install,
            f"docs pages offer no {scheme} palette option",
        )
    require("cadasto-by" in install, "copyright partial did not render on a docs page")
    require("cadasto-mark.png" in install, "company mark is not referenced from docs pages")

    require(ADD_COMMAND in read(QUICK_START), "pages/quick-start.md is missing the marketplace add command")
    require(ADD_COMMAND in read(INSTALL), "docs/install.md is missing the marketplace add command")
    require(ADD_COMMAND in quick, "quick-start page is missing the marketplace add command")
    require(ADD_COMMAND in install, "install page is missing the marketplace add command")
    require("skills-dir" in install, "install page is missing the local-development steps")
    require("info@cadasto.com" in contact, "contact page is missing the company email")
    for fact in ("Alkmaar", "98762893", "NL868632867B01"):
        require(fact in contact, f"contact page is missing {fact}")
    require(
        not re.search(r"<textarea|type=\"email\"", contact),
        "contact page has a form",
    )
    require("make docs-check" in contributing, "contributing page does not name make docs-check")
    require("make docs-serve" in contributing, "contributing page does not name make docs-serve")

    manifest = json.loads(read(MANIFEST))
    sources = json.loads(read(SOURCES))["sources"]
    names = [plugin["name"] for plugin in manifest["plugins"]]
    require(names, "marketplace.json has no plugins")
    by_source = {source["name"]: source for source in sources}
    for name in names:
        require(name in choose, f"choose page does not mention {name}")
        require(name in index, f"landing page does not mention {name}")
        page = read(SITE / "plugins" / name / "index.html")
        source = by_source[name]
        marker = f"Fetched from {source['repo']}@{source['ref']}:{source['path']}"
        require(marker in page, f"plugins/{name} is missing the fetched README ({marker})")
        require(f"/plugin install {name}@cadasto" in page, f"plugins/{name} is missing its install command")

    remote_fonts = []
    for path in SITE.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix not in {".html", ".css", ".js", ".txt"}:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        if re.search(r"https?://fonts\.(googleapis|gstatic)\.com", text):
            remote_fonts.append(str(path.relative_to(SITE)))
        if re.search(r'(href|src)="[^":]*\.md"', text):
            fail(f"unresolved relative .md path in {path.relative_to(SITE)}")
    require(not remote_fonts, "remote font URLs in output: " + ", ".join(remote_fonts[:8]))
    font_sheets = list(FONT_DIR.rglob("*")) if FONT_DIR.is_dir() else []
    font_text = "\n".join(
        path.read_text(encoding="utf-8", errors="replace")
        for path in font_sheets
        if path.is_file()
    )
    require(
        "font-display:swap" in font_text.replace(" ", ""),
        "no localised font sheet with font-display: swap",
    )
    for weight in ("500", "700"):
        require(
            re.search(rf"font-weight:\s*{weight}", font_text),
            f"no Fira Sans {weight} face was localised",
        )
    require(
        any(WOFF_DIR.rglob("*.woff2")) if WOFF_DIR.is_dir() else False,
        "the stylesheet was localised but no .woff2 binary was",
    )

    llms = read(SITE / "llms.txt")
    for slug in slugs:
        url = page_url(site_url, slug)
        require(url in llms, f"llms.txt does not link the {slug} page ({url})")
    require("CHANGELOG.md" in llms, "llms.txt does not link CHANGELOG.md")

    robots = read(SITE / "robots.txt")
    require(site_url + "sitemap.xml" in robots, "robots.txt does not name the sitemap")
    require((SITE / "sitemap.xml").is_file(), "sitemap.xml was not emitted")
    require("marketplace add" in index, "landing page is missing the marketplace add command")
    print("docs-check: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
