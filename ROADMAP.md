# Roadmap

## Why keep going

The rotation logic itself has been done since the early commits — what's
still being built here is packaging discipline: a small, real PyPI library
taken all the way through uv/ruff/mypy/pre-commit/twine, not just a script
that works on one machine. That's worth finishing precisely because it's
small; a clean, fully-shipped example is more useful as a reference than
another half-finished tool.

## What it opens up

Once the TestPyPI publish is green, this becomes the answer to "how do I
actually ship a Python package from this account" — a question several
other repos gesture at (`[private]` exists but has never
published anything real). A working, published `simple-api-key-rotator`
is proof the packaging path works end to end, not just in theory.

## Capability this builds

The publish-pipeline debugging done here (trusted publishing, version
bumping discipline, TestPyPI's immutable-version rejection) is exactly
the friction `[private]` is meant to save someone from later —
this repo is where that knowledge gets earned first.

## Connects to

- **[private]** — this repo is the real-world proof the
  template's packaging pattern actually works; once published, port the
  working publish workflow back into the template.
- **[private]** — stores the keys this rotates; any repo hitting a rate
  limit on a rotatable API (`[private]`'s YouTube quota,
  `[private]`) is a candidate consumer once this is a real package.
