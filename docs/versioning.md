# Versioning and Releases

This catalog carries its own version in `metadata.version`, independent of the versions of the plugins it lists. It uses [Semantic Versioning](https://semver.org), read from the perspective of **someone who has installed from it**.

| Bump | When |
|------|------|
| **Major** | A plugin is removed or renamed — `<name>@cadasto` breaks for everyone who has it installed |
| **Minor** | A plugin is added, or an entry is repinned to a plugin's new **minor or major** release |
| **Patch** | An entry is repinned to a plugin's **patch** release; or catalog metadata, docs, and tooling change with no effect on what installs |

## Does a plugin release bump the marketplace?

**Yes — and it has to.** Entries are pinned to release tags, so a plugin tagging `v0.5.0` reaches nobody until this catalog changes `version` and `source.ref`. That edit changes what installs, which is exactly what `metadata.version` tracks.

The two version lines stay independent: `sdd` going `0.4.0 → 0.5.0` is a *minor* bump to `sdd` and a *minor* bump to the catalog, but `sdd` going `0.4.0 → 1.0.0` is a *major* bump to `sdd` and still only a **minor** bump to the catalog — the catalog added a new version of something, it did not break any install id. Only removals and renames are catalog-major, because only those break `<name>@cadasto`.

Changes that touch no entry — a docs fix, a validator improvement, tightening CI — are catalog **patch** bumps. They alter the repository, not the catalog.

### The plugin-side consequence

Each plugin repo's own release checklist must now end with **"update the entry in `Cadasto/plugin-marketplace`"**. Before pinning, the catalog tracked default branches and a plugin release propagated on its own; it no longer does. A plugin release that stops at `git push --follow-tags` is invisible to users.

## The catalog cannot pin itself

Users add this repository with `/plugin marketplace add Cadasto/plugin-marketplace`, which tracks the **default branch**. There is no version pin at the marketplace level — that asymmetry is inherent, not an oversight.

Two consequences:

- **`main` is always live.** A broken manifest on `main` reaches every user on their next `/plugin marketplace update`. CI gates the merge for exactly this reason.
- **Tags here are informational.** Tag releases for traceability and changelog anchoring, but nothing consumes them the way `source.ref` consumes a plugin's tags.

## Release steps

1. Make the catalog change in `.claude-plugin/marketplace.json` — see [authoring.md](authoring.md).
2. Bump `metadata.version` per the table above.
3. Update the README table if the plugin list changed.
4. Fold the change into a dated `## [X.Y.Z] - YYYY-MM-DD` section in [CHANGELOG.md](../CHANGELOG.md) (Keep a Changelog — groups in order Added, Changed, Deprecated, Removed, Fixed, Security).
5. Run `python3 scripts/validate.py --fix` and `claude plugin validate .`.
6. **Smoke-test the Claude Code install** — see [testing.md](testing.md). Validation cannot tell you whether the pinned tag exists. Cursor installs from each plugin repo, not from this catalog.
7. Commit (`chore(release): vX.Y.Z`) and tag: `git tag -a vX.Y.Z -m "plugin-marketplace vX.Y.Z"`.
8. Push commits and the tag: `git push origin main --follow-tags`.

## History note

`1.2.1` recorded a plugin rename (`go-coding-plugin` → `go-coding`) as a patch. Under the table above that is a **major** bump: a rename changes the install id. The historical entry is left as it shipped; the rule applies going forward.
