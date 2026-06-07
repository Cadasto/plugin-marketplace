# Cadasto Plugin Marketplace

A [Claude Code](https://docs.anthropic.com/en/docs/claude-code) plugin marketplace maintained by [Cadasto B.V.](https://github.com/Cadasto)

## What is this?

Claude Code supports **plugins** — extensions that add new skills, commands, and tools to your coding assistant. Plugins can teach Claude Code about specific domains, connect it to external services, or give it specialized workflows tailored to your needs.

A **marketplace** is a curated catalog of plugins that you can browse, install, and keep up to date — all from within Claude Code. This marketplace collects the plugins built and maintained by Cadasto.

## Available Plugins

| Plugin                                                                           | Description                                                                  |
|----------------------------------------------------------------------------------|------------------------------------------------------------------------------|
| [openehr-assistant](https://github.com/Cadasto/openehr-assistant-plugin)         | AI plugin to assist on various openEHR related tasks                         |
| [openehr-assistant-dev](https://github.com/Cadasto/openehr-assistant-dev-plugin) | Maintainer plugin for developing the openEHR Assistant MCP server and plugin |

## Getting Started

First, add the Cadasto marketplace to your Claude Code installation. You only need to do this once:

```bash
/plugin marketplace add Cadasto/plugin-marketplace
```

Then install any plugin from the catalog:

```bash
/plugin install openehr-assistant@cadasto
```

To check for plugin updates later:

```bash
/plugin marketplace update cadasto
```

## License

[MIT](LICENSE)
