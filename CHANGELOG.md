# Changelog

All notable changes to this catalog will be documented in this file.

The format is based on Keep a Changelog, and this project adheres to Semantic Versioning.

- Keep a Changelog: https://keepachangelog.com/en/1.1.0/
- Semantic Versioning: https://semver.org/spec/v2.0.0.html

Versions here track the **catalog**, not the plugins it lists — see [docs/versioning.md](docs/versioning.md).

## [Unreleased]

## [1.4.0] - 2026-08-24

Turns the catalog from a list of repository names into a pinned, dual-host, machine-checked one. Entries now name a version and resolve to a release tag instead of a moving default branch.

### Added
- Cursor: `.cursor-plugin/marketplace.json` — the catalog published for Cursor. Generated from the Claude manifest (`$schema` dropped), never hand-edited. Cursor users could not add this marketplace at all before.
- Manifest: `version`, `displayName`, `author`, `homepage`, `license`, `category`, and `keywords` on every entry. `description`, `version`, and `keywords` are copied verbatim from each plugin's own `plugin.json`.
- Manifest: `source.ref` pinning every entry to its release tag — `openehr-assistant` `v0.9.0`, `openehr-assistant-dev` `v0.2.0`, `go-coding` `v0.4.0`, `sdd` `v0.4.0`.
- Manifest: top-level `$schema` and `owner.url`.
- Validation: `scripts/validate.py` — entry completeness, release-tag pinning and `version`/`ref` agreement, marketplace-level field placement, Cursor-twin sync, README-table agreement, and changelog coverage of `metadata.version`. `--fix` regenerates the twin. Stdlib only.
- CI: `.github/workflows/validate.yml` runs the validator on every push and pull request.
- Docs: `docs/install.md`, `docs/authoring.md`, `docs/testing.md`, `docs/versioning.md`, and this changelog.

### Changed
- Manifest: the marketplace `description` moved from `metadata` to the top level, where Claude Code reads it. `metadata.version` stays as the catalog's own release counter.
- Manifest: repository references normalised to the `Cadasto/…` casing.
- Manifest: `openehr-assistant-dev`'s description restored to the full text from its `plugin.json`.
- `README.md`: documents both hosts, the release-pinning rule, and how to contribute a catalog change.
- `AGENTS.md`: replaced the minimal entry template — which had been reproducing incomplete entries — with the full format, the pinning rule, and the release procedure.

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
