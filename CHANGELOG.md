# Changelog

All notable changes to this catalog will be documented in this file.

The format is based on Keep a Changelog, and this project adheres to Semantic Versioning.

- Keep a Changelog: https://keepachangelog.com/en/1.1.0/
- Semantic Versioning: https://semver.org/spec/v2.0.0.html

Versions here track the **catalog**, not the plugins it lists — see [docs/versioning.md](docs/versioning.md).

## [Unreleased]

### Changed
- Docs: the Cursor caveat — this catalog is not a Cursor marketplace — is stated once in `README.md` and once in `docs/install.md`, in the Cursor section each time, rather than twice per file.
- Docs: `docs/authoring.md` points at the remote tag check before a pin is committed; `docs/testing.md` records the `source.repo` shape the validator enforces.
- Docs: slash-command blocks are tagged `text`, shell blocks `bash`; Claude Code links use `docs.claude.com`.

### Fixed
- Docs: `docs/install.md` — the local-development install named `claude plugin add`, which is not a Claude Code command. Replaced with loading the working copy from `~/.claude/skills/<name>/`.
- Docs: `docs/versioning.md` — release step 9 passed a prose placeholder to `gh release create --notes-file`. It now pipes the CHANGELOG section in through `-F -`.

## [1.5.0] - 2026-08-25

### Added
- Plugins: `docs-editing` — documentation, editing and content standards (`Cadasto/docs-editing-plugin`), pinned to `v0.2.0`.
- Docs: `docs/versioning.md`, `AGENTS.md` — tag and release naming rules: annotated `vX.Y.Z` tags, a GitHub release per tag titled exactly the tag name, never move a published tag, plus the repair procedure for a mis-named tag.

### Changed
- Manifest: marketplace `description` names the documentation and content standards plugin.
- Releases: tags `1.2.0`, `1.2.1`, `1.3.0` re-cut as annotated `v1.2.0`, `v1.2.1`, `v1.3.0` at their original commits and the bare refs deleted; GitHub releases backfilled for every historical tag.

## [1.4.0] - 2026-08-25

### Added
- Cursor: generated `.cursor-plugin/marketplace.json` (Claude manifest minus `$schema`).
- Manifest: `version`, `displayName`, `author`, `homepage`, `license`, `category`, and `keywords` on every entry.
- Manifest: `source.ref` pins `openehr-assistant` `v0.9.0`, `openehr-assistant-dev` `v0.2.0`, `go-coding` `v0.4.0`, `sdd` `v0.4.0`.
- Manifest: top-level `$schema` and `owner.url`.
- CI: `scripts/validate.py` checks entry completeness, release-tag pinning, `version`/`ref` agreement, field placement, twin sync, README names and order, and changelog coverage of `metadata.version`.
- CI: `.github/workflows/validate.yml` runs the validator on every push and pull request.
- Docs: `docs/install.md`, `docs/authoring.md`, `docs/testing.md`, `docs/versioning.md`, and this changelog.

### Changed
- Manifest: marketplace `description` moved from `metadata` to the top level. `metadata.version` stays as the catalog release counter.
- Manifest: repository references normalised to the `Cadasto/…` casing.
- Manifest: `openehr-assistant-dev` description restored to the `plugin.json` text.
- Manifest: `$schema` points at `https://json.schemastore.org/claude-code-marketplace.json`.
- Docs: Cursor install is per plugin repo. This catalog is the Claude Code marketplace.

### Fixed
- Validation: `source.source` other than `github` is an error; pin checks always run.

## [1.3.0] - 2026-06-18

### Added
- Plugins: `sdd` — Spec-Driven Development workflow (`Cadasto/sdd-plugin`).

## [1.2.1] - 2026-06-14

### Changed
- Plugins: renamed `go-coding-plugin` to `go-coding`, matching the plugin's own manifest name. Recorded as a patch at the time; under the current rules a rename is a major bump (see [docs/versioning.md](docs/versioning.md#history-note)).

## [1.2.0] - 2026-06-13

### Added
- Plugins: `go-coding-plugin` — idiomatic Go coding standards (`Cadasto/go-coding-plugin`).

## [1.1.0] - 2026-06-07

### Added
- Plugins: `openehr-assistant-dev` — maintainer plugin for the openEHR Assistant MCP server and plugin (`Cadasto/openehr-assistant-dev-plugin`).

## [1.0.0] - 2026-03-16

### Added
- Initial catalog: marketplace manifest, `openehr-assistant`, README, and contributor guidance in `AGENTS.md`.
