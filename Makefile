# Uses uv (https://docs.astral.sh/uv) for dependency management — uv sync creates/updates .venv; run commands via uv run, no manual activation.
.PHONY: install test run lock help

install:
	uv sync --dev

test: install
	uv run pytest -q

# Entry point: this is a library, not an app — running it means running the test suite.
run: test

lock:
	uv lock

help:
	@echo "install - install dependencies"
	@echo "test    - run tests"
	@echo "run     - alias for test (entry point; library has no CLI)"
	@echo "lock    - update uv.lock"
