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
    fields = getattr(obj, FIELDS_NAME)
    init_args = {f.name: getattr(obj, f.name) for f in fields.values() if f.init}
    for name, new_value in changes.items():
        field = fields.get(name)
        if not field:
            raise TypeError(f"Unknown field: {name}")
        if not field.init:
            raise ValueError(f"Cannot replace field defined with init=False: {name}")
        init_args[name] = new_value
    return (type(obj))(**init_args)
