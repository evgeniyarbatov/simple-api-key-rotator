.PHONY: test

test:
		python3 -m venv .venv
		. .venv/bin/activate && python -m pip install -e .[test]
		. .venv/bin/activate && pytest -q
