import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from simple_api_key_rotator import (
    DEFAULT_ROOT_ENV,
    get_key,
    last_used_key,
    load_keys,
    load_usage,
    resolve_root,
    set_key,
)


def write_keys(path: Path, lines: list[str]) -> None:
    path.write_text("\n".join(lines) + "\n")


def write_usage(path: Path, usage: dict[str, str]) -> None:
    path.write_text(json.dumps(usage))


def test_load_keys_ignores_comments_and_blank_lines(tmp_path: Path) -> None:
    keys_path = tmp_path / "keys.txt"
    keys_path.write_text("""

# comment
key-a
  
key-b
# another
""".strip())

    assert load_keys(keys_path) == ["key-a", "key-b"]


def test_load_usage_missing_or_empty(tmp_path: Path) -> None:
    usage_path = tmp_path / "usage.json"
    assert load_usage(usage_path) == {}

    usage_path.write_text("   ")
    assert load_usage(usage_path) == {}


def test_last_used_key_selects_latest() -> None:
    keys = ["a", "b", "c"]
    usage = {
        "a": "2025-01-01T00:00:00+00:00",
        "c": "2025-01-03T00:00:00+00:00",
    }
    assert last_used_key(keys, usage) == "c"


def test_resolve_root_uses_env_var(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setenv(DEFAULT_ROOT_ENV, str(tmp_path))
    assert resolve_root() == tmp_path.resolve()


def test_get_key_returns_last_used(tmp_path: Path) -> None:
    service_dir = tmp_path / "service"
    service_dir.mkdir()
    write_keys(service_dir / "keys.txt", ["a", "b"])
    write_usage(
        service_dir / "usage.json",
        {"b": "2025-01-02T00:00:00+00:00"},
    )

    assert get_key("service", root=tmp_path) == "b"


def test_get_key_returns_first_when_no_usage(tmp_path: Path) -> None:
    service_dir = tmp_path / "service"
    service_dir.mkdir()
    write_keys(service_dir / "keys.txt", ["a", "b"])

    assert get_key("service", root=tmp_path) == "a"


def test_set_key_rotates_to_next_eligible(tmp_path: Path) -> None:
    service_dir = tmp_path / "service"
    service_dir.mkdir()
    write_keys(service_dir / "keys.txt", ["a", "b", "c"])

    now = datetime.now(timezone.utc)
    usage = {
        "a": (now - timedelta(hours=1)).isoformat(),
        "b": (now - timedelta(hours=25)).isoformat(),
    }
    write_usage(service_dir / "usage.json", usage)

    chosen = set_key("service", root=tmp_path)
    assert chosen == "b"

    updated = json.loads((service_dir / "usage.json").read_text())
    assert "b" in updated
    assert updated["b"] != usage["b"]


def test_set_key_errors_when_no_eligible(tmp_path: Path) -> None:
    service_dir = tmp_path / "service"
    service_dir.mkdir()
    write_keys(service_dir / "keys.txt", ["a", "b"])

    now = datetime.now(timezone.utc)
    usage = {
        "a": (now - timedelta(hours=1)).isoformat(),
        "b": (now - timedelta(hours=2)).isoformat(),
    }
    write_usage(service_dir / "usage.json", usage)

    with pytest.raises(RuntimeError, match="No key is eligible"):
        set_key("service", root=tmp_path)


def test_set_key_allows_custom_cooldown(tmp_path: Path) -> None:
    service_dir = tmp_path / "service"
    service_dir.mkdir()
    write_keys(service_dir / "keys.txt", ["a", "b"])

    now = datetime.now(timezone.utc)
    usage = {
        "a": (now - timedelta(hours=3)).isoformat(),
    }
    write_usage(service_dir / "usage.json", usage)

    chosen = set_key("service", root=tmp_path, cooldown_hours=2)
    assert chosen == "a"


def test_set_key_rejects_negative_cooldown(tmp_path: Path) -> None:
    service_dir = tmp_path / "service"
    service_dir.mkdir()
    write_keys(service_dir / "keys.txt", ["a"])

    with pytest.raises(ValueError, match="cooldown_hours"):
        set_key("service", root=tmp_path, cooldown_hours=-1)
