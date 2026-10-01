---
title: Cadasto plugins for Claude Code and Cursor
description: >-
  Six plugins for Claude Code and Cursor, each pinned to a release tag:
  openEHR modelling, spec-driven development, Go and PHP standards, and
  documentation. Add the marketplace once, then install by name.
hide:
  - navigation
  - toc
template: home.html
---

<div class="home-hero" markdown="1">

![](assets/logo.svg){ .home-hero__mark }

# Cadasto Plugin Marketplace

<p class="home-tagline">
Plugins that teach Claude Code and Cursor a specific job:<br>
openEHR modelling, spec-driven development,<br>
Go and PHP standards, and documentation.
</p>

<div class="home-cta" markdown="1">

[Add the marketplace](quick-start.md){ .md-button .md-button--primary }
[Choose a plugin](choose.md){ .md-button }
[View on GitHub](https://github.com/Cadasto/plugin-marketplace){ .md-button }

</div>

<p class="home-reassure" markdown="1">
MIT-licensed. Every entry names a release tag, so an install is never a branch tip. Cursor installs each plugin from its own repository.
</p>

</div>

<h2 class="section-title">The plugins</h2>

<div class="features-grid" markdown="1">

<div class="feature-card" markdown="1">

:material-heart-pulse:

### openEHR Assistant
Loads the relevant implementation guide before it answers, and searches CKM for archetypes and templates through a hosted MCP server. Covers archetypes, templates, compositions, and AQL.

[Plugin page](plugins/openehr-assistant.md){ .md-button }

</div>

<div class="feature-card" markdown="1">

:material-hammer-wrench:

### openEHR Assistant Dev
For the people who build the openEHR Assistant: authoring guides, prompts, MCP tools, and examples, and cutting releases of the server and plugin.

[Plugin page](plugins/openehr-assistant-dev.md){ .md-button }

</div>

<div class="feature-card" markdown="1">

:material-language-go:

### Go coding standards
Each skill names the tool that enforces a rule (`gofmt`, `go vet`, `golangci-lint`) and cites the style guide a judgement call comes from. A reviewer agent reports what the linters miss.

[Plugin page](plugins/go-coding.md){ .md-button }

</div>

<div class="feature-card" markdown="1">

:material-code-tags:

### PHP coding standards
PER Coding Style, PHPStan level 8, and PHP 8.4 idioms. A reviewer agent reports what the tools miss.

[Plugin page](plugins/php-coding.md){ .md-button }

</div>

<div class="feature-card" markdown="1">

:material-file-document-check-outline:

### Spec-driven development
`sdd-check` follows the chain from requirement to specification, ADR, code, and test in both directions, and fails the build on drift. The delivery pipeline runs on the same documents.

[Plugin page](plugins/sdd.md){ .md-button }

</div>

<div class="feature-card" markdown="1">

:material-text-box-edit-outline:

### Docs editing
Refuses to invent a statistic, testimonial, or superlative, and runs Vale on what it writes when Vale is installed. Covers technical writing, copy editing, AI-tell cleanup, SEO, and AI citability.

[Plugin page](plugins/docs-editing.md){ .md-button }

</div>

</div>

<h2 class="section-title">Why a catalog</h2>

<div class="features-grid" markdown="1">

<div class="feature-card" markdown="1">

:material-shield-check:

### Pinned, not tracking
Each entry names a version and the matching `vX.Y.Z` tag. A plugin that tags a release reaches nobody until this catalog moves, and a check fails the build when an entry's version and tag disagree.

</div>

<div class="feature-card" markdown="1">

:material-package-variant:

### One id per plugin
Add the marketplace once. After that, every install is `<plugin>@cadasto`, and an update is `/plugin marketplace update cadasto` followed by `/plugin update <plugin>`. You get the version this catalog names, not a branch tip.

</div>

<div class="feature-card" markdown="1">

:material-cube-outline:

### Claude Code and Cursor
Each plugin ships a manifest for both hosts from one set of skills and agents. Claude Code installs from this catalog. On Cursor, you install from the plugin's own repository.

</div>

<div class="feature-card" markdown="1">

:material-book-open-variant:

### Open and separate
Every plugin lives in its own repository under the MIT licence. This repository holds only the catalog and this site, and the site fetches each plugin's README at its pinned tag.

</div>

<div class="feature-card" markdown="1">

:material-toolbox:

### Needs stated up front
Most plugins are Markdown and JSON with no build step. The ones that use more, such as a hosted MCP server, a Go toolchain, or Python for the drift gate, say so on [Choose a plugin](choose.md#what-each-plugin-needs).

</div>

<div class="feature-card" markdown="1">

:material-file-check:

### Checked on every change
CI validates the manifest and its Cursor copy, and runs a prose check over the docs, on every pull request and every push to `main`. Claude Code users track `main`, so a broken manifest would be live at once.

</div>

</div>

<h2 class="section-title">Where you install them</h2>

<div class="two-products" markdown="1">

<div class="product-card" markdown="1">

:material-console:

### Claude Code
Add this marketplace once. Install any listed plugin as `<plugin>@cadasto`.

[Quick start](quick-start.md){ .md-button }

</div>

<div class="product-card" markdown="1">

:material-monitor:

### Cursor
Install each plugin from its own repository. Importing this catalog finds nothing to install.

[Cursor install](install.md#cursor){ .md-button }

</div>

</div>

<div class="quick-start" markdown="1">

## Quick start

```text
/plugin marketplace add Cadasto/plugin-marketplace
/plugin install <plugin>@cadasto
```

Restart the session to load the plugin. Not sure which one? [Choose by job](choose.md), or read how [updates and Cursor](install.md) work.

</div>
