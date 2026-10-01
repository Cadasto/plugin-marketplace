# Documentation site

This page is for maintainers building or changing the public site. Visitors read the published pages. The catalog rules stay in [authoring.md](authoring.md), [testing.md](testing.md), and [versioning.md](versioning.md).

The site is a MkDocs Material project in `pages/`, `mkdocs.yml`, and `overrides/main.html`. Colours, type, the landing template, the docs footer, and the company mark come from [docs-theme](https://github.com/Cadasto/docs-theme) at the commit `sources.json` pins. `make docs-sync` fetches those files into gitignored paths. Do not edit the copies.

## Preview and check

The preview needs Docker. The image is `squidfunk/mkdocs-material:9.7.6`.

```bash
make docs-serve   # http://127.0.0.1:8000
make docs-check   # strict build, then the output checks CI runs
make help
```

`docker compose up` is the same preview as `make docs-serve`. Prefer the Make target: it passes your user id into Compose, so you own the files the build writes.

`make docs-check DOCS_SYNC=docs-sync-offline` rebuilds from `.fetched/` and the brand files already on disk. The sync script refuses a cached brand file from a different `theme.ref`. Nothing in `.fetched/` or the brand paths survives `make docs-clean`.

## What the build fetches

`sources.json` has two pins:

- `theme.ref` is a commit. `ref_tag` is a label the scripts do not read. To move the brand layer, resolve the docs-theme tag to a commit and replace `ref` and each file's `sha256`.
- Each `sources` entry is one plugin README. `repo` and `ref` must equal that plugin's `source` in `.claude-plugin/marketplace.json`. `scripts/catalog_pins.py` fails the build when they differ.

`scripts/catalog_pins.py` also writes `.fetched/catalog.md` (the table on the plugins page) and `.fetched/catalog-install.md` (this repository's [install.md](install.md), with links rewritten for the site). The install page includes that file, so the steps have one home.

Plugin pages under `pages/plugins/` include the fetched README. When you add, repin, rename, or remove a plugin, update `sources.json`, the page, and the `nav` in `mkdocs.yml` in the same change. [authoring.md](authoring.md) is the catalog half of that edit.

## Publish

`.github/workflows/docs-ci.yml` runs `make docs-check` on pull requests into `main`. `.github/workflows/docs-site.yml` publishes `main` to GitHub Pages, and runs again weekly so a moved upstream file fails the build before the next edit here. The repository's Pages source has to be GitHub Actions. The site URL is `https://cadasto.github.io/plugin-marketplace/`.

`pages/llms.txt` lists every page in the nav. `scripts/check_site.py` fails the build when a nav entry is missing from it.

## Plugin repository access

Every listed plugin repository is public, so the fetch from `raw.githubusercontent.com` needs no token. `scripts/sync_sources.py` still sends `GH_TOKEN` or `GITHUB_TOKEN` when one is set, and the `Makefile` and both workflows set `GH_TOKEN` for it, so a private plugin repository would keep working: without a token, GitHub returns 404 for a private README. The workflows read the Actions secret `DOCS_SYNC_TOKEN` for that purpose. It is not needed while every plugin repository is public.
