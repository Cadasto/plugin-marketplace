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

Each plugin repo's own release checklist ends with one more step: **update the entry in `Cadasto/plugin-marketplace`**. Before pinning, the catalog tracked default branches and a plugin release propagated on its own; it no longer does. A plugin release that stops at `git push --follow-tags` is invisible to users.

## The catalog cannot pin itself

Users add this repository with `/plugin marketplace add Cadasto/plugin-marketplace`, which tracks the **default branch**. The marketplace level carries no version pin — that asymmetry is inherent, not an oversight.

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
9. Cut the GitHub release from the tag, titled **exactly** the tag name, with the new CHANGELOG section as the body. `-F -` reads that body from standard input. Set `VER` to the release being cut (for example `1.6.0`) — the same value drives the heading match, the tag, and the title:

   ```bash
   VER=1.6.0
   awk -v ver="$VER" '
     $0 ~ "^## \\[" ver "\\]" {f=1; next}
     /^## \[/ {f=0}
     f
   ' CHANGELOG.md | gh release create "v$VER" --title "v$VER" -F -
   ```

## Tag and release naming

These are rules, not preferences — a mixed history has to be repaired by moving published refs, which is worse than getting it right once.

- **Tags are `vX.Y.Z`.** Always the `v` prefix; never a bare `X.Y.Z`. This matches every Cadasto plugin repo, so one convention covers the whole org.
- **Tags are annotated** (`git tag -a`), never lightweight. An annotated tag carries its own author, date, and message.
- **Every tag has a GitHub release**, and the release title is **exactly** the tag name — `v1.4.0`, not `Release 1.4.0` or a themed name. The CHANGELOG section is the release body; the theme belongs there, not in the title.
- **Never reuse or move a published tag.** Cut the next patch instead.

If a tag ever lands in the wrong form, repair it by creating the correctly named annotated tag at the *same commit*, pushing it, verifying it is on the remote, and only then deleting the old ref — locally and remotely. Check first whether a release is attached to the old tag; if so, recreate it against the new one.

## History note

`1.2.1` recorded a plugin rename (`go-coding-plugin` → `go-coding`) as a patch. Under the table above that is a **major** bump: a rename changes the install id. The historical entry is left as it shipped; the rule applies going forward.

Tags `1.2.0`, `1.2.1`, and `1.3.0` originally shipped bare and lightweight, while `v1.0.0` and `v1.1.0` were annotated and prefixed. At the `v1.4.0` release the three were re-cut as annotated `v`-prefixed tags at their original commits and the bare refs deleted, and GitHub releases were backfilled for every historical tag. Release bodies before `v1.4.0` are empty — the CHANGELOG holds that history.
