---
description: >-
  Which Cadasto plugin to install: openEHR modelling, the assistant's
  maintainer tools, Go, PHP, spec-driven development, or documentation. Each
  plugin's requirements are listed.
---

# Choose a plugin

Install the plugin that matches the job. The install id in the table is the name you pass to `/plugin install`.

| When this is the job | Install |
|---|---|
| Author or review openEHR archetypes, templates, compositions, or AQL, or search CKM and the specifications | [`openehr-assistant`](plugins/openehr-assistant.md) |
| Add guides, MCP tools, examples, or releases to the openEHR Assistant server or plugin | [`openehr-assistant-dev`](plugins/openehr-assistant-dev.md) |
| Have an assistant write or review Go | [`go-coding`](plugins/go-coding.md) |
| Have an assistant write or review PHP | [`php-coding`](plugins/php-coding.md) |
| Keep a repository's specification as the source of truth, with stable ids for requirements and decisions | [`sdd`](plugins/sdd.md) |
| Have an assistant write or edit human-facing documentation, marketing copy, or search metadata | [`docs-editing`](plugins/docs-editing.md) |

A repository can use more than one. `sdd` owns specifications and traceability, and hands language review to the reviewer a repository declares, such as `go-coding`'s `go-reviewer`. `docs-editing` writes prose for people and leaves specifications to `sdd`. `openehr-assistant-dev` is for people building the openEHR Assistant; clinical modelling is `openehr-assistant`.

## What each plugin needs

Every plugin installs from Markdown and JSON, with no build step. What differs is what it can use once it is installed, and what you keep if that is missing.

| Plugin | Works fully with | Without it |
|---|---|---|
| `openehr-assistant` | A reachable openEHR Assistant MCP server. The default install bundles a config for the hosted one. | The guide-first workflows have nothing to load. The `clinical-modeler` agent falls back to the offline reference material in the plugin. |
| `openehr-assistant-dev` | Checkouts of the openEHR Assistant server and plugin repositories, the projects it maintains. | It has no other target. For clinical modelling, use `openehr-assistant`. |
| `go-coding` | Go 1.26.4 or newer, with `gofmt`, `gofumpt`, `goimports`, and `gopls` on `PATH`, and golangci-lint v2 for full-tree linting. | The skills still guide the assistant. The format-on-save hook does nothing when no formatter is installed. |
| `php-coding` | PHP 8.4 or newer, with `php-cs-fixer`, `phpstan`, and `phpunit` in the project. | The skills still guide the assistant; nothing enforces them. Laravel framework code is outside this plugin. |
| `sdd` | Python 3.9 or newer for the vendored drift gate, and a build entry point with a `spec-check` target. `gh`, or `az` with the `azure-devops` extension, mirrors findings to pull requests. | Everything runs on the local findings file. |
| `docs-editing` | [Vale](https://vale.sh), so the prose rules are machine-checked. | The skills apply the standards by judgment, and the prose-lint hook stays silent. |

On Cursor, you install each plugin from its own repository; [Install](install.md#cursor) shows how. The catalog pins a release tag, so an install never follows a plugin's default branch. [The plugin list](plugins/index.md) shows the tag each entry names.
