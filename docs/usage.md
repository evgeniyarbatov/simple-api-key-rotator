# Usage Guide

## Directory layout

Each service has its own folder containing `keys.txt` and (optionally) `usage.json`:

```
./my-service/
  keys.txt
  usage.json
```

- `keys.txt` holds one key per line.
- Blank lines are ignored.
- Lines starting with `#` are treated as comments and ignored.

## Basic usage

```python
from simple_api_key_rotator import get_key, set_key

# Read the most recently used key, or the first key if none were used yet.
current = get_key("my-service")

# Rotate to the next eligible key and record usage time.
next_key = set_key("my-service")
```

## Root directory selection

You can set a custom base directory in two ways:

1. Use the `API_KEY_ROTATOR_ROOT` environment variable.
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

## Example: rotate on 429 responses

Rotate the key when the API returns a rate-limit error.

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
