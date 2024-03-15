from .decorator import FIELDS, dataclass
from .field import MISSING, Field, FrozenInstanceError, field

VERSION = "0.0.0"
"""Read and written by the ``hatch version`` command."""

__all__ = [
    "Field",
    "FrozenInstanceError",
    "MISSING",
    "dataclass",
    "field",
    "fields",
    "is_dataclass",
]


def is_dataclass(obj: object) -> bool:
    """Check if an object or class is a dataclass."""
    cls = obj if isinstance(obj, type) else type(obj)
    return hasattr(cls, FIELDS)


def fields(obj: object) -> tuple[Field, ...]:
    """Retrieve all the Fields of an object or class."""
    cls = obj if isinstance(obj, type) else type(obj)
    return tuple(getattr(cls, FIELDS).values())
