"""Module-level dataclasses functions."""

from .constants import FIELDS_NAME
from .field import Field

try:
    from typing import Any, TypeVar

    T = TypeVar("T")
except ImportError:
    pass


def is_dataclass(obj: object) -> bool:
    """Check if an object or class is a dataclass."""
    cls = obj if isinstance(obj, type) else type(obj)
    return hasattr(cls, FIELDS_NAME)


def fields(obj: object) -> tuple[Field, ...]:
    """Retrieve all the Fields of an object or class."""
    cls = obj if isinstance(obj, type) else type(obj)
    return tuple(getattr(cls, FIELDS_NAME).values())


def replace(obj: T, **changes: Any) -> T:
    """Create a new object with the specified fields replaced."""
    # TODO(dhrosa): init-only and init=False fields must be handled specially.
    # Note: MicroPython key views don't support set operations directly.
    names = set(getattr(obj, FIELDS_NAME).keys())
    if unknown_names := set(changes.keys()) - names:
        raise TypeError(f"Unknown field names: {unknown_names}")
    init_args = {name: getattr(obj, name) for name in names}
    return (type(obj))(**(init_args | changes))
