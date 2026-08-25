# Cadasto Plugin Marketplace

A plugin marketplace maintained by [Cadasto B.V.](https://github.com/Cadasto) for [Claude Code](https://docs.anthropic.com/en/docs/claude-code). Every listed plugin also ships a [Cursor](https://cursor.com/docs/plugins) manifest, so the same plugins install on Cursor from each plugin repository.

## What is this?

Claude Code and Cursor both support **plugins** — extensions that add new skills, commands, and tools to your coding assistant. Plugins can teach the assistant about specific domains, connect it to external services, or give it specialized workflows tailored to your needs.

A **marketplace** is a curated catalog of plugins that you can browse, install, and keep up to date — all from within your assistant. This marketplace collects the plugins built and maintained by Cadasto.

This catalog is the Claude Code marketplace. Its source of truth is `.claude-plugin/marketplace.json`. `.cursor-plugin/marketplace.json` is generated from that file (`$schema` dropped) for field parity. Cursor's own marketplace schema expects plugins that live in this repository, so adding this repo in Cursor does not install the remote plugins.

## Available Plugins

| Plugin                                                                           | Description                                                                  |
|----------------------------------------------------------------------------------|------------------------------------------------------------------------------|
| [openehr-assistant](https://github.com/Cadasto/openehr-assistant-plugin)         | AI plugin to assist on various openEHR related tasks                         |
| [openehr-assistant-dev](https://github.com/Cadasto/openehr-assistant-dev-plugin) | Maintainer plugin for developing the openEHR Assistant MCP server and plugin — authoring guides, prompts, MCP tools, examples, and managing releases |
| [go-coding](https://github.com/Cadasto/go-coding-plugin)                         | Idiomatic Go coding standards for AI assistants — formatting, errors, concurrency, testing, layout. |
| [sdd](https://github.com/Cadasto/sdd-plugin)                                     | Spec-Driven Development workflow for AI assistants — requirements, RFC-2119 specs, ADRs, and plans with stable identifiers, machine-checked traceability, and drift CI. |
| [docs-editing](https://github.com/Cadasto/docs-editing-plugin)                   | Human-facing documentation and content standards for AI assistants — technical writing, copy editing, marketing copy, SEO and AI citability, with claims grounded in cited evidence. |

## Getting Started

### Claude Code

Add the Cadasto marketplace. You only need to do this once:

```bash
/plugin marketplace add Cadasto/plugin-marketplace
```

Then install any plugin from the catalog:

```bash
/plugin install openehr-assistant@cadasto
```

To pick up new plugins and released versions later:

```bash
/plugin marketplace update cadasto
```

### Cursor

Install each plugin from its own repository — this catalog is not a Cursor marketplace of remote plugins. Cursor's [Team Marketplace](https://cursor.com/docs/plugins) indexes plugins that live in the imported repo. Each Cadasto plugin ships `.cursor-plugin/plugin.json` and can be added locally or submitted on its own. See [docs/install.md](docs/install.md).

## Releases

Catalog entries are pinned to a release tag (`vX.Y.Z`) rather than tracking a default branch, so installing a plugin gives you a released version and never an in-flight commit. Publishing a new plugin version therefore takes two steps: tag the release in the plugin repo, then bump `version` and `source.ref` in this catalog.

## Documentation

| Document | Covers |
|----------|--------|
| [docs/install.md](docs/install.md) | Adding the Claude Code marketplace, and installing the same plugins on Cursor |
| [docs/authoring.md](docs/authoring.md) | The catalog entry format, and adding, updating, renaming or removing a plugin |
| [docs/testing.md](docs/testing.md) | Validating the manifests and smoke-testing a real install |
| [docs/versioning.md](docs/versioning.md) | How the catalog is versioned, and the release procedure |
| [CHANGELOG.md](CHANGELOG.md) | What changed in each catalog release |

[AGENTS.md](AGENTS.md) is the working brief for AI assistants maintaining this repository.

## Contributing

Adding or updating a plugin means editing `.claude-plugin/marketplace.json`, then regenerating the Cursor twin and verifying everything:

```bash
python3 scripts/validate.py --fix
```

CI runs the same script on every push and pull request. See [docs/authoring.md](docs/authoring.md) for the entry format and [docs/versioning.md](docs/versioning.md) for the release steps.

## License

[MIT](LICENSE)
