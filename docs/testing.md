# Testing and Validation

This is a manifest-only repository — no build step, no package manager, no runtime. "Testing" means proving the catalog is well-formed, internally consistent, and that what it points at actually installs.

## Automated checks

```bash
python3 scripts/validate.py        # the full check — what CI runs
python3 scripts/validate.py --fix  # regenerate the Cursor twin, then check
claude plugin validate .           # Claude Code's own schema validator
```

### `scripts/validate.py`

Stdlib only — no network, no auth, no dependencies — so CI runs it directly and it works offline. It checks:

- **Marketplace shape** — `$schema`, top-level `description` and `owner` (with `url`), kebab-case name, and that nothing but `version` sits under `metadata`.
- **Entry completeness** — every field in the [entry format](authoring.md#entry-format) is present, names are kebab-case and unique, `version` is semver, `keywords` is non-empty.
- **Release pinning** — `source.ref` exists, is a `vX.Y.Z` tag, and matches the entry's `version`. This is the check that stops an unpinned entry from silently shipping a plugin's default branch.
- **Cursor twin** — `.cursor-plugin/marketplace.json` equals the Claude manifest minus `$schema`. Drift is an error, not a warning; `--fix` regenerates it.
- **README table** — lists the same plugins in the same order as the manifest.
- **Changelog** — `metadata.version` has a matching `## [X.Y.Z]` section.

A failure names the file and the field, e.g. `plugins[2] (go-coding): source.ref 'v0.3.0' does not match version '0.4.0'`.

### `claude plugin validate .`

Complements the above rather than duplicating it: it knows the real manifest schema and **warns on unknown fields** (`Unknown field 'foo'. Claude Code ignores it at load time.`), which is the fastest way to catch a typo'd key that `validate.py` would not recognise as wrong. Run both before committing.

## Manual smoke test

Validation proves the manifest is well-formed. It cannot prove the pinned tag exists or that the plugin installs — nothing here reaches the network. Before releasing a catalog change, install for real:

```
/plugin marketplace add Cadasto/plugin-marketplace     # or: update cadasto
/plugin install <plugin>@cadasto
```

Then confirm:

- The plugin appears in `claude plugin list` attributed to `cadasto`.
- `claude plugin details <plugin>` shows the expected components — and the version matches the catalog entry, not something newer. A newer version means the pin is not being honoured.
- `/plugin` shows the plugin under its `category` with its `displayName` and description.
- The equivalent install works in **Cursor** (Settings → Plugins), since the twin is what Cursor reads.

### Verifying a pin before committing

The tag must exist on the remote, or the entry installs nothing:

```bash
git ls-remote --tags https://github.com/Cadasto/<repo>.git | grep 'v1.2.3$'
```

## CI

`.github/workflows/validate.yml` runs `scripts/validate.py` on every push and pull request. Because users track this repository's **default branch** — a catalog cannot pin itself — a broken `main` is live immediately. Keep `main` releasable at all times, and let CI gate the merge.
