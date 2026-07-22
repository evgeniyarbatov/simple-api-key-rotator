# Uses uv (https://docs.astral.sh/uv) for dependency management — uv sync creates/updates .venv; run commands via uv run, no manual activation.
.PHONY: install test lock help

install:
	uv sync --dev

test: install
	uv run pytest -q

lock:
	uv lock

help:
	@echo "install - install dependencies"
	@echo "test    - run tests"
	@echo "lock    - update uv.lock"
