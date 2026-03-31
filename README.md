# Simple API Key Rotator

Rotate API keys using a 24-hour cooldown rule. Keys are stored in a text file and usage is tracked in a JSON file per service.

## Installation

```bash
pip install simple-api-key-rotator
```

## Quickstart

```python
from simple_api_key_rotator import get_key, set_key

current = get_key("my-service")
next_key = set_key("my-service")
```

## Directory layout

Create a directory per service with a `keys.txt` file and (optionally) a `usage.json` file:

```
./my-service/
  keys.txt
  usage.json
```

`keys.txt` example:

```
# Comments and blank lines are ignored
key-1
key-2
key-3
```

## Root directory selection

You can set the base directory in two ways:

1. Set `API_KEY_ROTATOR_ROOT` in the environment.
2. Pass `root=...` to `get_key` or `set_key`.

```python
from pathlib import Path
from simple_api_key_rotator import get_key

key = get_key("my-service", root=Path("/srv/api-keys"))
```

If both are provided, the explicit `root=` argument wins.

## Rotation rules

A key is eligible when:

- It has never been used, or
- It was last used more than 24 hours ago.

When rotating, the algorithm starts from the key after the most recently used key and wraps around in order.

## Error cases

`get_key` and `set_key` raise `RuntimeError` when no key is eligible or `keys.txt` is empty.

## Documentation

- `docs/README.md`
- `docs/usage.md`
- `docs/api.md`

## Development

```bash
python -m pip install -e .[test]
pytest -q
```
