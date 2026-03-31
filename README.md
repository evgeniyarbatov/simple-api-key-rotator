# Simple API Key Rotator

Rotate API keys using a cooldown rule (default 24 hours). Keys are stored in a text file and usage is tracked in a JSON file per service.

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
- It was last used more than 24 hours ago (by default).

When rotating, the algorithm starts from the key after the most recently used key and wraps around in order.

You can override the cooldown window:

```python
from simple_api_key_rotator import set_key

next_key = set_key("my-service", cooldown_hours=6)
```

## Error cases

`get_key` and `set_key` raise `RuntimeError` when no key is eligible or `keys.txt` is empty.

## Example: rotate on API exceptions

Rotate the key when an API returns a rate-limit response, then retry or exit.

```python
import requests

from simple_api_key_rotator import get_key, set_key


def call_api():
    api_key = get_key("my-service")
    response = requests.get(
        "https://api.example.com/endpoint",
        params={"q": "example", "key": api_key},
    )

    if response.status_code == 429:
        set_key("my-service")
        raise RuntimeError("Rate limited. Rotated key; retry later.")

    response.raise_for_status()
    return response.json()
```

## Documentation

- `docs/README.md`
- `docs/usage.md`
- `docs/api.md`

## Development

```bash
python -m pip install -e .[test]
pytest -q
```
