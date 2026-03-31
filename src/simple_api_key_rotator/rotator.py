from __future__ import annotations

import json
import os
from datetime import datetime, timedelta, timezone
from pathlib import Path

DEFAULT_ROOT_ENV = "API_KEY_ROTATOR_ROOT"


def resolve_root(root: Path | str | None = None) -> Path:
    if root is None:
        env_root = os.environ.get(DEFAULT_ROOT_ENV)
        if env_root:
            return Path(env_root).expanduser().resolve()
        return Path.cwd()
    return Path(root).expanduser().resolve()


def service_paths(service: str, root: Path | str | None = None) -> tuple[Path, Path]:
    base = resolve_root(root) / service
    keys_path = base / "keys.txt"
    usage_path = base / "usage.json"
    return keys_path, usage_path


def load_keys(keys_path: Path) -> list[str]:
    lines = keys_path.read_text().splitlines()
    return [line.strip() for line in lines if line.strip() and not line.strip().startswith("#")]


def load_usage(usage_path: Path) -> dict[str, str]:
    if not usage_path.exists():
        return {}
    content = usage_path.read_text().strip()
    if not content:
        return {}
    return json.loads(content)


def save_usage(usage_path: Path, usage: dict[str, str]) -> None:
    usage_path.parent.mkdir(parents=True, exist_ok=True)
    usage_path.write_text(json.dumps(usage, indent=2, sort_keys=True))


def last_used_key(keys: list[str], usage: dict[str, str]) -> str | None:
    last_key = None
    last_time = None
    for key in keys:
        last_used = usage.get(key)
        if not last_used:
            continue
        used_at = datetime.fromisoformat(last_used)
        if last_time is None or used_at > last_time:
            last_time = used_at
            last_key = key
    return last_key


def get_key(service: str, root: Path | str | None = None) -> str:
    keys_path, usage_path = service_paths(service, root=root)
    keys = load_keys(keys_path)
    usage = load_usage(usage_path)

    key = last_used_key(keys, usage)
    if key:
        return key
    if not keys:
        raise RuntimeError("No key is eligible based on the 24-hour rule")
    return keys[0]


def set_key(
    service: str,
    root: Path | str | None = None,
    cooldown_hours: float = 24,
) -> str:
    keys_path, usage_path = service_paths(service, root=root)
    keys = load_keys(keys_path)
    usage = load_usage(usage_path)
    if cooldown_hours < 0:
        raise ValueError("cooldown_hours must be >= 0")

    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(hours=cooldown_hours)

    if not keys:
        raise RuntimeError("No key is eligible based on the cooldown rule")

    current = last_used_key(keys, usage)
    start_index = keys.index(current) + 1 if current in keys else 0

    for offset in range(len(keys)):
        key = keys[(start_index + offset) % len(keys)]
        last_used = usage.get(key)
        if not last_used:
            usage[key] = now.isoformat()
            save_usage(usage_path, usage)
            return key
        if datetime.fromisoformat(last_used) <= cutoff:
            usage[key] = now.isoformat()
            save_usage(usage_path, usage)
            return key

    raise RuntimeError("No key is eligible based on the cooldown rule")
