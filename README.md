# Cadasto Plugin Marketplace

A plugin marketplace maintained by [Cadasto B.V.](https://github.com/Cadasto), for [Claude Code](https://docs.anthropic.com/en/docs/claude-code) and [Cursor](https://cursor.com/docs/plugins).

## What is this?

Claude Code and Cursor both support **plugins** — extensions that add new skills, commands, and tools to your coding assistant. Plugins can teach the assistant about specific domains, connect it to external services, or give it specialized workflows tailored to your needs.

A **marketplace** is a curated catalog of plugins that you can browse, install, and keep up to date — all from within your assistant. This marketplace collects the plugins built and maintained by Cadasto.

Every plugin here ships manifests for both hosts, and the catalog is published twice from a single source of truth: `.claude-plugin/marketplace.json` for Claude Code and `.cursor-plugin/marketplace.json` for Cursor.

## Available Plugins

| Plugin                                                                           | Description                                                                  |
|----------------------------------------------------------------------------------|------------------------------------------------------------------------------|
| [openehr-assistant](https://github.com/Cadasto/openehr-assistant-plugin)         | AI plugin to assist on various openEHR related tasks                         |
| [openehr-assistant-dev](https://github.com/Cadasto/openehr-assistant-dev-plugin) | Maintainer plugin for developing the openEHR Assistant MCP server and plugin |
| [go-coding](https://github.com/Cadasto/go-coding-plugin)                         | Idiomatic Go coding standards for AI assistants (formatting, errors, concurrency, testing, layout) |
| [sdd](https://github.com/Cadasto/sdd-plugin)                                     | Spec-Driven Development workflow — requirements, RFC-2119 specs, ADRs, and plans with stable identifiers, traceability, and drift CI |

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

Add this repository as a plugin marketplace from **Settings → Plugins**, then install any plugin from the catalog. Cursor reads `.cursor-plugin/marketplace.json` at the repository root, and each plugin repo carries its own `.cursor-plugin/plugin.json`.

## Releases

Catalog entries are pinned to a release tag (`vX.Y.Z`) rather than tracking a default branch, so installing a plugin gives you a released version and never an in-flight commit. Publishing a new plugin version therefore takes two steps: tag the release in the plugin repo, then bump `version` and `source.ref` in this catalog.

## Contributing

Adding or updating a plugin means editing `.claude-plugin/marketplace.json`, then regenerating the Cursor twin and verifying everything:

```bash
python3 scripts/validate.py --fix
```

CI runs the same script on every push and pull request. See [AGENTS.md](AGENTS.md) for the full entry format and conventions.

## License

[MIT](LICENSE)
