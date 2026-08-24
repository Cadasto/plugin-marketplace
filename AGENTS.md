# AGENTS.md

Instructions for Claude Code and subagents working in this repository.

## Project

This is the **Cadasto Plugin Marketplace** — a plugin catalog maintained by Cadasto B.V., serving both **Claude Code** and **Cursor**. It is a catalog only: every plugin lives in its own repository and is referenced here by a pinned release tag. Nothing here is a plugin component; if you are writing a skill, agent, command, or hook, you are in the wrong repository.

## Structure

| Path | Role |
|------|------|
| `.claude-plugin/marketplace.json` | **Source of truth.** Every catalog change starts here. |
| `.cursor-plugin/marketplace.json` | **Generated** — the Claude manifest minus `$schema`. Never hand-edit. |
| `README.md` | Human-facing entry point; its plugin table mirrors the manifest. |
| `CHANGELOG.md` | Per-release catalog history (Keep a Changelog). |
| `docs/` | The detailed guides — see the table below. |
| `scripts/validate.py` | The full check; `--fix` regenerates the Cursor twin. |
| `.github/workflows/validate.yml` | Runs the validator on every push and PR. |

Marketplace name: `cadasto` — users install with `/plugin install <plugin>@cadasto`.

## Where things are documented

Keep detail in `docs/` and keep this file a brief. When a convention changes, update the doc that **owns** it and leave the others pointing at it — do not restate a rule in two places.

| Document | Owns |
|----------|------|
| [docs/install.md](docs/install.md) | Install and update flows, both hosts; local development installs |
| [docs/authoring.md](docs/authoring.md) | Entry format, field provenance, add / update / rename / remove |
| [docs/testing.md](docs/testing.md) | What each validator checks; the manual smoke test |
| [docs/versioning.md](docs/versioning.md) | Catalog SemVer rules, plugin-vs-catalog bumps, release steps |

## Making a catalog change

1. Edit the `plugins` array in `.claude-plugin/marketplace.json`. The full entry format is in [docs/authoring.md](docs/authoring.md#entry-format) — every field there is required, and `description`, `version`, and `keywords` are copied **verbatim** from the plugin's own `plugin.json`.
2. Pin `source.ref` to the `vX.Y.Z` tag matching the entry's `version`.
3. Mirror the change in the README table (same plugins, same order).
4. Bump `metadata.version` and add a `CHANGELOG.md` entry.
5. Run `python3 scripts/validate.py --fix` and `claude plugin validate .`.

Steps 3, 4, and 5 are enforced — validation fails on a README mismatch, on a `metadata.version` with no changelog section, and on a stale Cursor twin.

### Reacting to a plugin release

A plugin repo tagging a release **does not ship it**. Entries are pinned, so users see nothing until this catalog moves. When told a plugin has released, bump that entry's `version` **and** `source.ref` together, then bump `metadata.version` and record it in the changelog. Do not bump one without the other; validation rejects a mismatch.

Verify the tag exists on the remote before pinning — nothing in the validator reaches the network:

```bash
git ls-remote --tags https://github.com/Cadasto/<repo>.git | grep 'v1.2.3$'
```

### Versioning

`metadata.version` is the **catalog's** version, independent of the plugins it lists. Full rules in [docs/versioning.md](docs/versioning.md); in short:

- **Major** — a plugin is removed or renamed (breaks `<name>@cadasto`)
- **Minor** — a plugin is added, or repinned to a new minor/major plugin release
- **Patch** — repinned to a plugin patch release; or docs, tooling, metadata changes that do not alter what installs

A plugin's own major bump is still only a catalog **minor** — the catalog gained a version, it did not break an install id.

### CHANGELOG style

- Entries accumulate under `## [Unreleased]` and fold into a dated `## [X.Y.Z] - YYYY-MM-DD` section at release.
- Keep a Changelog groups in order — **Added, Changed, Deprecated, Removed, Fixed, Security** — omitting empty groups.
- One terse line per bullet; lead with the subsystem (`Manifest:`, `Plugins:`, `Cursor:`, `Docs:`, `CI:`) and use backticks for file, field, and plugin names. No rationale or PR links — that belongs in the commit message.

## Validation

```bash
python3 scripts/validate.py     # conventions, Cursor twin, README table, changelog (what CI runs)
claude plugin validate .        # Claude Code's own schema validator
```

Run both. The second one warns about unknown fields, which is the fastest way to catch a typo'd key that `validate.py` has no rule for. See [docs/testing.md](docs/testing.md) for what each covers and why validation alone is not sufficient before a release.

## Key Conventions

- Plugin names are kebab-case, unique, and must match the plugin's own `name` — it is the install id
- Repository references use the `Cadasto/…` casing consistently
- `description`, `version`, `keywords` are copied verbatim from the plugin's `plugin.json`; if the wording is poor, fix it **in the plugin repo** and let it flow here on the next release
- `category` is not enum-validated — a typo passes silently and drops the plugin from that filter. Use an established value (`development`, `productivity`, `security`, `testing`, …)
- Marketplace `description` and `owner` live at the top level; the only field under `metadata` is `version`
- A plugin with no `vX.Y.Z` release tag cannot be pinned, so it does not belong in the catalog yet

### Commit Messages
- Follow [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/), e.g. `feat(plugins): add sdd to the catalog`, `fix(manifest): correct source repo for plugin-x`, `chore(release): v1.4.0`.
- Scopes: `plugins`, `manifest`, `cursor`, `docs`, `ci`.

## Gotchas

- **The catalog cannot pin itself.** Users track this repo's default branch, so a broken `main` is live immediately. Keep `main` releasable; let CI gate the merge.
- **`.cursor-plugin/marketplace.json` is generated.** Editing it directly gets silently overwritten by the next `--fix`. Change the Claude manifest instead.
- **An unpinned entry is a supply-chain hole, not a convenience.** Without `source.ref` every push to a plugin's default branch ships straight to every installed user.
- **The plugin repos' own release docs need a final step** pointing back here. Before pinning existed the catalog tracked default branches, and some plugin `docs/versioning.md` files still say a marketplace update is unnecessary.
