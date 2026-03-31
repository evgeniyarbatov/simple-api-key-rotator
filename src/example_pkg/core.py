from __future__ import annotations


def greet(name: str) -> str:
    """Return a friendly greeting.

    Args:
        name: The person's name.

    Raises:
        ValueError: If the name is empty or only whitespace.
    """
    cleaned = name.strip()
    if not cleaned:
        raise ValueError("name must be non-empty")
    return f"Hello, {cleaned}!"
