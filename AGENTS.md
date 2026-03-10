# AGENTS.md

Instructions for Claude Code and subagents working in this repository.

## Project

This is the **Cadasto Plugin Marketplace** — a Claude Code plugin marketplace maintained by Cadasto B.V. It serves as a catalog for discovering and installing Cadasto plugins via Claude Code's plugin system.

## Structure

- `.claude-plugin/marketplace.json` — The marketplace manifest. This is the core file that defines the marketplace identity and lists all available plugins. Single source of truth for all registered plugins.
- Marketplace name: `cadasto`

## Adding Plugins

To register a new plugin, add an entry to the `plugins` array in `.claude-plugin/marketplace.json`. Each entry requires at minimum `name`, `source`, and `description`. Use the GitHub source format for plugins hosted on GitHub:

```json
{
  "name": "plugin-name",
  "description": "Brief description",
  "source": {
    "source": "github",
    "repo": "cadasto/plugin-repo"
  }
}
```

### Documentation Sync
When adding, removing, or renaming plugins, update: **`.claude-plugin/marketplace.json`** (plugin entries), **`README.md`** (plugin table), and **`AGENTS.md`** (if conventions or structure changed).

## Validation

```bash
claude plugin validate .
```

## Key Conventions

- Plugin names use kebab-case and must be unique within the marketplace
- Marketplace name is `cadasto` — users install with `/plugin install <plugin>@cadasto`
- Use the GitHub source format (`"source": "github", "repo": "cadasto/plugin-repo"`) for plugins hosted on GitHub

### Commit Messages
- Follow [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/), e.g. `feat(plugins): added openehr-assistant plugin`, `fix(manifest): corrected source repo for plugin-x`.
- Scopes: `plugins`, `manifest`, `docs`.
