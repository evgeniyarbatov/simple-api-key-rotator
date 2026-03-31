# High-Quality Package Checklist

Use this as a pre-release and ongoing maintenance checklist.

## Project basics

- Clear package name and import name
- Short, accurate description and keywords
- License chosen and included
- Version defined (Semantic Versioning)

## Code quality

- Public API documented and stable
- Type hints for public functions
- Errors validated with helpful messages
- No unused code or dead imports

## Tests

- Unit tests cover happy path and edge cases
- Regression tests for bugs
- Coverage reported and reviewed
- Tests run on multiple Python versions

## Documentation

- README includes installation, usage, and development steps
- API usage examples included
- Docs build succeeds (MkDocs or equivalent)

## Packaging

- `python -m build` succeeds
- `python -m twine check dist/*` passes
- Wheels and source distributions included
- Package installs cleanly from wheel

## Security & maintenance

- Security contact documented
- Dependency updates reviewed regularly
- Changelog maintained for user-visible changes

## Release

- Version bumped and changelog updated
- Tests, lint, and type checks pass
- Tag created and pushed
- PyPI upload verified
