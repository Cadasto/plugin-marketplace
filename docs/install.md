# Installing from the Cadasto Marketplace

> This repository is a **catalog**, not a plugin. It contains no skills, agents, or commands — only the manifests that tell Claude Code and Cursor where the Cadasto plugins live and which release to install.

The catalog is published twice from a single source of truth: `.claude-plugin/marketplace.json` for [Claude Code](https://docs.claude.com/en/docs/claude-code/plugins) and `.cursor-plugin/marketplace.json` for [Cursor](https://cursor.com/docs/plugins). Both list the same plugins at the same pinned versions.

## Claude Code

### Add the marketplace

```
/plugin marketplace add Cadasto/plugin-marketplace
```

Once only. The marketplace name is `cadasto`, so its plugins are addressed as `<plugin>@cadasto`.

### Install a plugin

```
/plugin install openehr-assistant@cadasto
/plugin install openehr-assistant-dev@cadasto
/plugin install go-coding@cadasto
/plugin install sdd@cadasto
```

### Update

```
/plugin marketplace update cadasto     # refresh the catalog itself
/plugin update <plugin>                # move a plugin to the catalog's current pin
```

A session restart is required for an update to take effect. Because entries are pinned (see [versioning.md](versioning.md)), `/plugin update` moves you to the version this catalog names — not to whatever is on the plugin repo's default branch.

### Inspect

```bash
claude plugin list                     # what is installed, and from which marketplace
claude plugin details <plugin>         # component inventory + projected token cost
```

## Cursor

Add this repository as a plugin marketplace from **Settings → Plugins**, then install any plugin from the catalog.

Cursor reads `.cursor-plugin/marketplace.json` at the repository root; each plugin repo carries its own `.cursor-plugin/plugin.json` declaring its `skills`, `agents`, `rules`, and `hooks` paths.

## Local development against a plugin

To work on a plugin itself, bypass the catalog and install from your working copy — this picks up uncommitted changes, which a pinned catalog entry deliberately will not:

```bash
claude plugin add /path/to/go-coding-plugin
```

See that plugin repo's own `docs/install.md` for its host requirements and hook wiring.

## What is in the catalog

The authoritative list is the manifest; [README.md](../README.md) mirrors it in a table, and CI checks the two agree. Each entry names the plugin's `version` and pins `source.ref` to the matching `vX.Y.Z` release tag, so installing gives you a released version and never an in-flight commit.
