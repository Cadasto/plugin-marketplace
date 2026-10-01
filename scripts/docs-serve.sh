#!/bin/sh
# Fetch pinned sources, then serve MkDocs. `docker compose up` runs this.
# `make docs-check` bypasses it and calls the Python scripts and MkDocs directly.
set -eu
cd /docs
python3 scripts/catalog_pins.py
python3 scripts/sync_sources.py
exec mkdocs serve -a 0.0.0.0:8000
