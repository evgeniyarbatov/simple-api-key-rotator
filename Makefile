.PHONY: test

test:
	python -m pip install -e .[test]
	pytest -q
