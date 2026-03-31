# Example PyPI Package Template

This repository is a complete, minimal template for a high-quality Python package suitable for release on PyPI. It includes a dummy implementation, tests, documentation scaffolding, and a release checklist.

## Customize the template

Replace the placeholder names before your first release:

- Project name: update `example_pkg` in `pyproject.toml` under `[project].name`.
- Import name: rename the `src/example_pkg` package directory and update imports.
- Version: update `[project].version` in `pyproject.toml`.
- Metadata: update authors, URLs, classifiers, and description in `pyproject.toml`.
- License: replace `LICENSE` if you need a different license.

Quick rename example:

```bash
mv src/example_pkg src/your_package
rg -l "example_pkg" | xargs sed -i '' -e 's/example_pkg/your_package/g'
```

## Install for development

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install -U pip
python -m pip install -e ".[dev]"
```

## Usage (dummy package sample)

```python
from example_pkg import greet

print(greet("Ada"))
```

## Tests

```bash
pytest
```

## Linting and formatting

```bash
ruff check .
ruff format .
```

## Type checks

```bash
mypy src
```

## Documentation

This template uses MkDocs for simple, fast docs.

```bash
mkdocs serve
```

To build the static site:

```bash
mkdocs build
```

Documentation lives in `docs/index.md`, and configuration is in `mkdocs.yml`.

## Build and verify the package

```bash
python -m build
python -m twine check dist/*
```

## Publish to TestPyPI

```bash
python -m twine upload --repository testpypi dist/*
```

## Publish to PyPI

Create a PyPI API token and set it in your environment:

```bash
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=pypi-REDACTED
```

Then upload the distribution:

```bash
python -m twine upload dist/*
```

## Release checklist

- Update version in `pyproject.toml` and `CHANGELOG.md`.
- Confirm metadata and URLs in `pyproject.toml` are accurate.
- Run tests: `pytest`.
- Run lint/format: `ruff check .` and `ruff format .`.
- Run type checks: `mypy src`.
- Build and verify artifacts: `python -m build` and `python -m twine check dist/*`.
- Test install from the wheel: `python -m pip install dist/*.whl`.
- Upload to TestPyPI and verify install: `pip install -i https://test.pypi.org/simple/ your-package`.
- Upload to PyPI.
- Tag the release in git.

## What is included

- `src/example_pkg` with a tiny implementation and type hints
- `tests` with unit tests and coverage config
- `docs` + `mkdocs.yml` for documentation
- `pyproject.toml` with build, test, lint, type-check, and package metadata
- `Makefile` helper commands
- `CHECKLIST.md` for quality and release gates
- `CHANGELOG.md`, `LICENSE`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, and `SECURITY.md`
- GitHub Actions CI workflow for tests and linting
