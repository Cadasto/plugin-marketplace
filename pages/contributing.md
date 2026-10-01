---
description: >-
  Build the Cadasto marketplace site locally, keep plugin README pins aligned
  with the catalog, and publish with GitHub Pages.
---

# Build the marketplace site

The public site is this MkDocs project. Product behaviour lives in each plugin repository. This repository holds the catalog and the pages that frame it.

## Preview

The preview needs Docker. The image pin is `squidfunk/mkdocs-material:9.7.6`, the same tag the other Cadasto docs sites build with.

```bash
make docs-serve
```

That fetches the pinned brand layer and plugin READMEs, then serves [http://127.0.0.1:8000](http://127.0.0.1:8000). `docker compose up` does the same thing. `make docs-serve` passes your user id into Compose so generated files stay yours.

```bash
make docs-check
```

`make docs-check` is the strict build CI runs. `make help` lists the other targets.

Maintainer detail, including an offline rebuild, is in the [site maintainer guide](https://github.com/Cadasto/plugin-marketplace/blob/main/docs/site.md) in this repository.

## Where a change goes

| Change | Edit |
|---|---|
| Add, repin, rename, or remove a plugin | The [catalog authoring guide](https://github.com/Cadasto/plugin-marketplace/blob/main/docs/authoring.md), then the matching `sources.json` entry, the page under `pages/plugins/`, and the nav in `mkdocs.yml` |
| Install steps for the catalog | The [catalog install guide](https://github.com/Cadasto/plugin-marketplace/blob/main/docs/install.md). The install page on this site includes that file |
| A plugin's own features | That plugin's repository. The site fetches its README at the catalog pin |

Catalog versioning and release tags are in the [versioning guide](https://github.com/Cadasto/plugin-marketplace/blob/main/docs/versioning.md).

## Issues

A wrong pin, a broken page, or the catalog manifest: [Cadasto/plugin-marketplace](https://github.com/Cadasto/plugin-marketplace). A bug in a plugin: that plugin's repository, linked from its page.
