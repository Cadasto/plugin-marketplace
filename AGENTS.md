# AGENTS.md

Instructions for Claude Code and subagents working in this repository.

## Project

This is the **Cadasto Plugin Marketplace** — a plugin marketplace maintained by Cadasto B.V., serving both **Claude Code** and **Cursor**. It is a catalog only: every plugin lives in its own repository and is referenced here by a pinned release tag.

## Structure

- `.claude-plugin/marketplace.json` — the marketplace manifest for Claude Code. **Single source of truth** for the catalog; every change starts here.
- `.cursor-plugin/marketplace.json` — the Cursor twin. **Generated, never hand-edited.** It is the Claude manifest with the `$schema` key dropped.
- `scripts/validate.py` — validates the manifest, regenerates and checks the Cursor twin, and checks the README table. Run with `--fix` to regenerate.
- `.github/workflows/validate.yml` — runs the validator on every push and pull request.
- Marketplace name: `cadasto`

## Adding or Updating a Plugin

Edit the `plugins` array in `.claude-plugin/marketplace.json`. Every entry carries the full set of fields below — `/plugin` uses them to present and filter the catalog, so none of them are optional here:

```json
{
  "name": "plugin-name",
  "displayName": "Plugin Name",
  "description": "Description, copied verbatim from the plugin's own plugin.json",
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

Then regenerate the Cursor twin and verify:

```bash
python3 scripts/validate.py --fix
```

### Release Pinning

`source.ref` **must** be a `vX.Y.Z` release tag matching `version`. An unpinned entry resolves to the plugin repo's default branch, which ships every push straight to every installed user with no release gate. The validator enforces both the tag format and the `version` ↔ `ref` match.

Publishing a new plugin version is therefore two steps: tag the release in the plugin repo, then bump `version` and `source.ref` here.

### Documentation Sync

When adding, removing, or renaming plugins, update **`.claude-plugin/marketplace.json`** (the entry and `metadata.version`), **`README.md`** (the plugin table — same plugins, same order; the validator checks this), and **`AGENTS.md`** (only if conventions or structure changed). `.cursor-plugin/marketplace.json` is regenerated, not edited.

## Validation

```bash
python3 scripts/validate.py     # conventions, Cursor twin, README table (what CI runs)
claude plugin validate .        # Claude Code's own schema validator
```

Both should pass before committing. The second one also warns about unknown fields, which is the fastest way to catch a typo'd key.

## Key Conventions

- Plugin names use kebab-case and must be unique within the marketplace
- Marketplace name is `cadasto` — users install with `/plugin install <plugin>@cadasto`
- Repository references use the `Cadasto/…` casing consistently (GitHub is case-insensitive, but the catalog should not be inconsistent with itself)
- `description`, `version`, and `keywords` are copied verbatim from the plugin's own `plugin.json`, so the catalog never disagrees with the plugin it points at
- `category` is not enum-validated by Claude Code — a typo passes silently. Use an established value (`development`, `productivity`, `security`, `testing`, …)
- Marketplace-level `description` and `owner` live at the top level, where Claude Code reads them. The one thing that stays under `metadata` is `version` — the catalog's own release counter, bumped whenever the plugin list changes (see the `chore(manifest): bump marketplace version` commits)

### Commit Messages
- Follow [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/), e.g. `feat(plugins): added openehr-assistant plugin`, `fix(manifest): corrected source repo for plugin-x`.
- Scopes: `plugins`, `manifest`, `docs`, `ci`.
