# Cadasto Plugin Marketplace

A Claude Code plugin marketplace maintained by [Cadasto B.V.](https://github.com/Cadasto)

## Available Plugins

| Plugin | Description | Version |
|--------|-------------|---------|
| [openehr-assistant](https://github.com/Cadasto/openehr-assistant-plugin) | AI plugin to assist on various openEHR related tasks | 0.2.1 |

## Installation

### Add the marketplace

```bash
# From Claude Code
/plugin marketplace add Cadasto/plugin-marketplace
```

### Install a plugin

```bash
# Install the openEHR assistant plugin
/plugin install openehr-assistant@cadasto
```

## For Developers

### Register a new plugin

1. Add a plugin entry to `.claude-plugin/marketplace.json`
2. Include at minimum: `name`, `source`, and `description`
3. Submit a pull request

### Validate the marketplace

```bash
claude plugin validate .
```

## License

MIT
