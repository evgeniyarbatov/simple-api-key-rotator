PYTHON ?= python3
VENV ?= .venv
PIP := $(VENV)/bin/pip
PY := $(VENV)/bin/python

.PHONY: venv install test lint format typecheck docs build publish

venv:
	$(PYTHON) -m venv $(VENV)
	$(PIP) install -U pip

install: venv
	$(PIP) install -e ".[dev]"

test:
	$(PY) -m pytest

lint:
	$(PY) -m ruff check .

format:
	$(PY) -m ruff format .

typecheck:
	$(PY) -m mypy src

docs:
	$(PY) -m mkdocs build

build:
	$(PY) -m build

publish:
	$(PY) -m twine upload dist/*
