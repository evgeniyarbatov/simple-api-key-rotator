# Uses uv (https://docs.astral.sh/uv) for dependency management — uv sync creates/updates .venv; run commands via uv run, no manual activation.
.PHONY: test lock help

test:
	uv sync --dev
	uv run pytest -q

lock:
	uv lock

help:
	@echo "test  - install dependencies and run tests"
	@echo "lock  - update uv.lock"
