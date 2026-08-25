# Installing from the Cadasto Marketplace

> This repository is a **catalog**, not a plugin. It contains no skills, agents, or commands — only the Claude Code marketplace manifest that names each Cadasto plugin and which release to install.

The source of truth is `.claude-plugin/marketplace.json` for [Claude Code](https://docs.claude.com/en/docs/claude-code/plugins). `.cursor-plugin/marketplace.json` is generated from it (`$schema` dropped) for field parity. Cursor's [marketplace schema](https://cursor.com/docs/reference/plugins) expects plugins that live in this repository, so adding this repo in Cursor does not install the remote plugins. Install those from each plugin repo — see [Cursor](#cursor).

## Claude Code

### Add the marketplace

```
/plugin marketplace add Cadasto/plugin-marketplace
```

Once only. The marketplace name is `cadasto`, so its plugins are addressed as `<plugin>@cadasto`.

### Install a plugin

```
/plugin install <plugin>@cadasto
```

The current names are in the [README plugin table](../README.md#available-plugins).

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

Install each plugin from its own repository. This catalog is the Claude Code marketplace; it does not contain plugin directories, so a Cursor [Team Marketplace](https://cursor.com/docs/plugins) import of this repo has nothing to resolve.

Each plugin repo ships `.cursor-plugin/plugin.json` (skills, agents, rules, hooks). Add that repo locally, or submit it on its own, following that repo's `docs/install.md`.

## Local development against a plugin

To work on a plugin itself, bypass the catalog and install from your working copy — this picks up uncommitted changes, which a pinned catalog entry deliberately will not:

```bash
claude plugin add /path/to/go-coding-plugin
```

See that plugin repo's own `docs/install.md` for its host requirements and hook wiring.

## What is in the catalog

The authoritative list is the Claude manifest. [README.md](../README.md) lists the same plugin names in the same order, and CI checks that agreement. Each entry names the plugin's `version` and pins `source.ref` to the matching `vX.Y.Z` release tag, so a Claude Code install gives you a released version and never an in-flight commit.
