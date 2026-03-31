# Contributing

Thanks for helping improve this project!

## Development setup

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install -U pip
python -m pip install -e ".[dev]"
```

## Running checks

```bash
pytest
ruff check .
ruff format .
mypy src
```

## Pull request checklist

- Add or update tests for your change.
- Update documentation if behavior changes.
- Update `CHANGELOG.md` for user-facing changes.
- Ensure `pytest`, `ruff`, and `mypy` pass.
