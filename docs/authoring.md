# Authoring Catalog Entries

Authoring in this repository means editing **one array**: `plugins` in `.claude-plugin/marketplace.json`. The Cursor twin is regenerated from it. The README table and changelog stay hand-edited and are checked against it.

## The single source of truth

| File | Role |
|------|------|
| `.claude-plugin/marketplace.json` | **Source of truth.** Every catalog change starts here. |
| `.cursor-plugin/marketplace.json` | **Generated.** The Claude manifest with `$schema` dropped, for field parity. Not Cursor's native multi-plugin schema. Never hand-edit it. |
| `README.md` (plugin table) | Same plugin names, same order — CI enforces names and order, not descriptions. |
| `CHANGELOG.md` | What changed in each catalog release. |

Regenerate and verify in one step:

```bash
python3 scripts/validate.py --fix
```

## Entry format

Every entry carries the full set of fields. None are optional here — `/plugin` uses them to present and filter the catalog, and an entry missing any of them fails validation:

```json
{
  "name": "plugin-name",
  "displayName": "Plugin Name",
  "description": "Copied verbatim from the plugin's own plugin.json",
  "version": "1.2.3",
  "author": { "name": "Cadasto B.V.", "url": "https://github.com/Cadasto" },
  "homepage": "https://github.com/Cadasto/plugin-repo",
  "license": "MIT",
  "category": "development",
  "keywords": ["keyword-one", "keyword-two"],
  "source": {
    "source": "github",
    "repo": "Cadasto/plugin-repo",
    "ref": "v1.2.3"
  }
}
```

### Where each field comes from

- **`description`, `version`, `keywords`** — copied **verbatim** from the plugin's own `.claude-plugin/plugin.json`. The catalog must never disagree with the plugin it points at. If a description reads poorly, fix it in the plugin repo and let it flow here on the next release; do not improve it only here.
- **`name`** — must match the plugin's own `name`. This is the install id (`<name>@cadasto`), so changing it breaks every existing install.
- **`source.ref`** — the `vX.Y.Z` release tag matching `version`. See [versioning.md](versioning.md).
- **`category`** — **not** enum-validated by Claude Code; a typo passes silently and quietly removes the plugin from that filter. Use an established value: `development`, `productivity`, `security`, `testing`, `database`, `monitoring`, `deployment`, `design`, `automation`, `learning`.
- **`displayName`** — the human-readable name shown in the catalog UI.

## Adding a plugin

1. Confirm the plugin repo is **releasable**: it has `.claude-plugin/plugin.json`, a `.cursor-plugin/plugin.json`, and at least one `vX.Y.Z` tag. A plugin with no release tag cannot be pinned, so it does not belong in the catalog yet.
2. Add the entry, copying `description` / `version` / `keywords` from its `plugin.json` and pinning `source.ref` to its latest tag.
3. Add a matching row to the README table, in the same position.
4. Bump `metadata.version` and add a `CHANGELOG.md` entry ([versioning.md](versioning.md)).
5. `python3 scripts/validate.py --fix`

## Updating a plugin to a new release

The plugin repo tagging a release does **not** ship it — pinned entries mean users see nothing until this catalog moves. Bump `version` and `source.ref` together (validation rejects a mismatch), then bump `metadata.version` and record it in the changelog.

## Renaming or removing a plugin

Both break `<name>@cadasto` for everyone who has it installed, and are **major** catalog bumps. Removing also orphans installs rather than uninstalling them, so say what replaced it in the changelog. Claude Code supports a top-level `renames` map for the rename case (Anthropic's own marketplace uses one) — prefer that over a bare rename if continuity matters.

## Marketplace-level fields

`description` and `owner` live at the **top level**. The one field under `metadata` is `version` — this catalog's own release counter. Claude Code also accepts `version` and `description` under `metadata`; this repo keeps them at the top level so the house rule stays one place. Do not move a marketplace description back under `metadata`; validation rejects it.

## What does not belong here

This repo ships no plugin components. If you find yourself writing a skill, agent, command, or hook, it belongs in a plugin repo — the catalog only points at them.
