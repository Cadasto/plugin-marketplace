---
description: >-
  Add the Cadasto marketplace in Claude Code, install a plugin by name, and
  update the catalog when a release is pinned.
---

# Add the marketplace

Add the Cadasto marketplace in Claude Code, then install one plugin by its catalog name.

## Requirements

Claude Code, with the `/plugin` command and network access to GitHub. Claude Code fetches each plugin from its `Cadasto/…` repository at the tag this catalog pins. Cursor installs each plugin from its own repository; [Install](install.md#cursor) covers that path.

## Add it and install a plugin

```text
/plugin marketplace add Cadasto/plugin-marketplace
```

Once. The marketplace name is `cadasto`, so a plugin's install id is its catalog name plus `@cadasto`.

```text
/plugin install <plugin>@cadasto
```

The names are on [Choose a plugin](choose.md) and the [plugin list](plugins/index.md). For example, the openEHR Assistant installs with:

```text
/plugin install openehr-assistant@cadasto
```

## What you have afterwards

The plugin's skills, agents, and commands load in the next session. Each plugin's page on the [plugin list](plugins/index.md) includes the README from the pinned release, which is where its own requirements live. openEHR Assistant, for example, registers a hosted MCP server; the others are Markdown and JSON and need no server.

Updates, inspection, Cursor, and loading a working copy while you develop a plugin are on [Install](install.md).
