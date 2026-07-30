# CLAUDE.md

## What this is

Python library that rotates API keys using a cooldown rule, so callers can
spread requests across multiple keys and avoid rate limits. Keys live in a
per-service `keys.txt`; usage is tracked in a per-service `usage.json`.

## Key files

- `simple_api_key_rotator/rotator.py` — rotation logic (`get_key`, `set_key`).
- `simple_api_key_rotator/__init__.py` — public API exports.
- `tests/test_rotator.py` — test suite.
- `docs/README.md` — extended documentation.

## How to run

```bash
make run
```

Library only, no CLI/app — `make run` runs the test suite (alias for
`make test`). `make install` sets up the `uv` virtualenv.

## Conventions / gotchas

- Dependency management via `uv`; run commands through `uv run`, don't
  activate the venv manually.
- Key files (`keys.txt`, `usage.json`) are user-supplied data, not part of
  this repo — never commit real API keys.
- Root directory for key files resolves via `API_KEY_ROTATOR_ROOT` env var
  or an explicit `root=` argument (explicit wins).
