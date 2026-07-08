.PHONY: test

test:
	uv venv .venv
	. .venv/bin/activate && python -m uv pip install -e .[test]
	.venv/bin/pytest -q
