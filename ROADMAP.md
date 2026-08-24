# Roadmap

Small, stable library: rotate API keys via a cooldown rule, keys in
`keys.txt`, usage tracked in `usage.json`. The core API (`get_key`,
`set_key`) has been feature-complete since the early commits — recent
history is tooling migration (uv, ruff/mypy, pre-commit), not new
capability.

## Next

- Get the TestPyPI publish green again (see [TODO.md](TODO.md)) — that's
  the only thing currently blocking a real release.
- No planned feature work beyond that; this is a finished small tool, not
  an active product.
