# Documentation

## Usage Guide

### Directory layout

Each service has its own folder containing `keys.txt` and (optionally) `usage.json`:

```
./my-service/
  keys.txt
  usage.json
```

- `keys.txt` holds one key per line.
- Blank lines are ignored.
- Lines starting with `#` are treated as comments and ignored.

### Basic usage

```python
from simple_api_key_rotator import get_key, set_key

# Read the most recently used key, or the first key if none were used yet.
current = get_key("my-service")

# Rotate to the next eligible key and record usage time.
next_key = set_key("my-service")
```

### Root directory selection

You can set a custom base directory in two ways:

1. Use the `API_KEY_ROTATOR_ROOT` environment variable.
2. Pass `root=...` to `get_key` or `set_key`.

```python
from pathlib import Path
from simple_api_key_rotator import get_key

key = get_key("my-service", root=Path("/srv/api-keys"))
```

If both are provided, the explicit `root=` argument wins.

### Rotation rules

A key is eligible when:

- It has never been used, or
- It was last used more than 24 hours ago (by default).

When rotating, the algorithm starts from the key after the most recently used key and wraps around in order.

You can override the cooldown window:

```python
from simple_api_key_rotator import set_key

next_key = set_key("my-service", cooldown_hours=6)
```

### Error cases

`get_key` and `set_key` raise `RuntimeError` when no key is eligible or `keys.txt` is empty.

### Example: rotate on 429 responses

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

## API Reference

### `get_key(service, root=None)`

Returns the most recently used key for the service. If no usage has been recorded, returns the first key listed in `keys.txt`.

Parameters:

- `service` (str): service folder name.
- `root` (Path | str | None): optional base directory. Defaults to `API_KEY_ROTATOR_ROOT` or the current working directory.

Raises `RuntimeError` when no keys are available.

### `set_key(service, root=None, cooldown_hours=24)`

Rotates to the next eligible key and records the usage timestamp in `usage.json` (UTC ISO 8601).

Parameters:

- `service` (str): service folder name.
- `root` (Path | str | None): optional base directory. Defaults to `API_KEY_ROTATOR_ROOT` or the current working directory.
- `cooldown_hours` (float): cooldown window in hours. Defaults to 24.

Returns the selected key as a string. Raises `RuntimeError` when no keys are eligible.

### `service_paths(service, root=None)`

Returns `(keys_path, usage_path)` for the service.

### `load_keys(keys_path)`

Loads keys from the given file, ignoring blank lines and comments.

### `load_usage(usage_path)`

Loads usage data from JSON. Returns an empty dict when the file is missing or empty.

### `save_usage(usage_path, usage)`

Writes usage data to JSON. Creates parent directories if they do not exist.

### `last_used_key(keys, usage)`

Returns the most recently used key from `usage` that is present in `keys`, or `None` if no usage exists.
