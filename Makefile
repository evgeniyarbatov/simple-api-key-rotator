.PHONY: test

test:
	uv venv .venv
	uv pip install -e .[test]
	.venv/bin/pytest -q
