# API Reference

## `get_key(service, root=None)`

Returns the most recently used key for the service. If no usage has been recorded, returns the first key listed in `keys.txt`.

Parameters:

- `service` (str): service folder name.
- `root` (Path | str | None): optional base directory. Defaults to `API_KEY_ROTATOR_ROOT` or the current working directory.

Raises `RuntimeError` when no keys are available.

## `set_key(service, root=None, cooldown_hours=24)`

Rotates to the next eligible key and records the usage timestamp in `usage.json` (UTC ISO 8601).

Parameters:

- `service` (str): service folder name.
- `root` (Path | str | None): optional base directory. Defaults to `API_KEY_ROTATOR_ROOT` or the current working directory.
- `cooldown_hours` (float): cooldown window in hours. Defaults to 24.

Returns the selected key as a string. Raises `RuntimeError` when no keys are eligible.

## `service_paths(service, root=None)`

Returns `(keys_path, usage_path)` for the service.

## `load_keys(keys_path)`

Loads keys from the given file, ignoring blank lines and comments.

## `load_usage(usage_path)`

Loads usage data from JSON. Returns an empty dict when the file is missing or empty.

## `save_usage(usage_path, usage)`

Writes usage data to JSON. Creates parent directories if they do not exist.

## `last_used_key(keys, usage)`

Returns the most recently used key from `usage` that is present in `keys`, or `None` if no usage exists.
