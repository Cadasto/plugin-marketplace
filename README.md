# Cadasto Plugin Marketplace

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-1.10.0-blue)](CHANGELOG.md)
[![Claude Code](https://img.shields.io/badge/Claude_Code-marketplace-D97757?logo=anthropic&logoColor=white)](https://docs.claude.com/en/docs/claude-code/plugins)
[![Cursor](https://img.shields.io/badge/Cursor-per--plugin_install-000?logo=cursor&logoColor=white)](https://cursor.com/docs/plugins)
[![Keep a Changelog](https://img.shields.io/badge/Keep%20a%20Changelog-1.1.0-E05735)](CHANGELOG.md)

The [Claude Code](https://docs.claude.com/en/docs/claude-code) plugin catalog maintained by [Cadasto B.V.](https://github.com/Cadasto), for Claude Code users who want Cadasto's plugins for openEHR clinical modeling, spec-driven development, Go coding standards, and documentation standards. A **plugin** extends a coding assistant with skills, commands, agents, and tools, teaching it a domain, connecting it to a service, or giving it a specific workflow. A **marketplace** is a catalog of plugins you browse, install, and update from inside the assistant. Add this one once and install any listed plugin as `<plugin>@cadasto`.

This repository is a catalog only. Each plugin lives in its own repository and is listed here pinned to a release tag, so an install gives you a released version. The source of truth is `.claude-plugin/marketplace.json`; `.cursor-plugin/marketplace.json` is generated from it for field parity. Every listed plugin also ships a [Cursor](https://cursor.com/docs/plugins) manifest, but Cursor installs each plugin from that plugin's own repository, not from this catalog.

**Requirements.** Claude Code with the `/plugin` command, and network access to GitHub: each plugin is fetched from its `Cadasto/…` repository at the pinned tag. Cursor users install from each plugin's repository instead; see [Cursor](#cursor). Individual plugins state their own host requirements in their repositories. Maintaining the catalog needs Python 3 (the validator uses only the standard library).

## Table of contents

- [Available Plugins](#available-plugins)
- [Installation](#installation)
- [Releases](#releases)
- [Development](#development)
- [Documentation](#documentation)
- [License](#license)

## Available Plugins

<!-- Descriptions are copied verbatim from each plugin's own plugin.json; see
     docs/authoring.md. Reword them in the plugin repo, never here. -->
<!-- vale write-good.Weasel = NO -->

| Plugin                                                                           | Description                                                                  |
|----------------------------------------------------------------------------------|------------------------------------------------------------------------------|
| [openehr-assistant](https://github.com/Cadasto/openehr-assistant-plugin)         | openEHR clinical modeling for AI assistants — archetypes, templates, compositions, AQL, CKM reuse search, and specification lookup.                         |
| [openehr-assistant-dev](https://github.com/Cadasto/openehr-assistant-dev-plugin) | Maintainer plugin for developing the openEHR Assistant MCP server and plugin — authoring guides, prompts, MCP tools, examples, and managing releases |
| [go-coding](https://github.com/Cadasto/go-coding-plugin)                         | Idiomatic Go coding standards for AI assistants — formatting, errors, concurrency, testing, layout. |
| [sdd](https://github.com/Cadasto/sdd-plugin)                                     | Spec-Driven Development for AI assistants — requirements, RFC-2119 specs, and ADRs with stable identifiers, machine-checked traceability, and the delivery pipeline that runs on them: plan, workers, review ledger, close-out. |
| [docs-editing](https://github.com/Cadasto/docs-editing-plugin)                   | Human-facing documentation and content standards for AI assistants: technical writing, copy editing, AI-tell cleanup, marketing copy, SEO and AI citability, with claims grounded in cited evidence. |

<!-- vale write-good.Weasel = YES -->

## Installation

### Claude Code

Add the Cadasto marketplace. You only need to do this once:

```text
/plugin marketplace add Cadasto/plugin-marketplace
```

Then install any plugin from the catalog:

```text
/plugin install openehr-assistant@cadasto
```

To pick up new plugins and released versions later:

```text
/plugin marketplace update cadasto
```

### Cursor

Install each plugin from its own repository. Cursor's [Team Marketplace](https://cursor.com/docs/plugins) indexes plugins that live in the repository you import, so importing this catalog of remote sources finds nothing to install. Each Cadasto plugin ships `.cursor-plugin/plugin.json` and is added on its own; see [docs/install.md](docs/install.md#cursor).

## Releases

Each catalog entry pins a release tag (`vX.Y.Z`) instead of tracking a default branch, so installing a plugin gives you a released version and never an in-flight commit. Publishing a new plugin version takes two steps: tag the release in the plugin repo, then bump `version` and `source.ref` in this catalog. Until the catalog moves, users keep the previous version.

## Development

Adding or updating a plugin means editing `.claude-plugin/marketplace.json`, then regenerating the Cursor twin and validating the result:

```bash
python3 scripts/validate.py --fix
```

Before committing, also run `claude plugin validate .`, Claude Code's own schema check; it warns on unknown fields and is not part of CI.

CI runs the same script, plus a Vale prose lint, on every pull request and every push to `main`. See [docs/testing.md](docs/testing.md) for what each check covers, [docs/authoring.md](docs/authoring.md) for the entry format, and [docs/versioning.md](docs/versioning.md) for the release steps.

## Documentation

| Document | Covers |
|----------|--------|
| [docs/install.md](docs/install.md) | Adding the Claude Code marketplace, and installing the same plugins on Cursor |
| [docs/authoring.md](docs/authoring.md) | The catalog entry format, and adding, updating, renaming, or removing a plugin |
| [docs/testing.md](docs/testing.md) | Validating the manifests and smoke-testing a real install |
| [docs/versioning.md](docs/versioning.md) | How the catalog is versioned, and the release procedure |
| [CHANGELOG.md](CHANGELOG.md) | What changed in each catalog release |

[AGENTS.md](AGENTS.md) is the working brief for AI assistants maintaining this repository.

## License

[MIT](LICENSE)
