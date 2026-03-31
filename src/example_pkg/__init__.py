from importlib.metadata import PackageNotFoundError, version as _version

from .core import greet

try:
    __version__ = _version("example_pkg")
except PackageNotFoundError:  # pragma: no cover - when running from source tree
    __version__ = "0.0.0"

__all__ = ["greet", "__version__"]
