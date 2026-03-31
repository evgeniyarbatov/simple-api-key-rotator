import pytest

from example_pkg.core import greet


def test_greet_happy_path() -> None:
    assert greet("Ada") == "Hello, Ada!"


def test_greet_strips_whitespace() -> None:
    assert greet("  Alan  ") == "Hello, Alan!"


def test_greet_rejects_empty() -> None:
    with pytest.raises(ValueError, match="non-empty"):
        greet("   ")
