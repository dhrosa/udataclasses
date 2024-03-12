from .dataclass import dataclass, fields, is_dataclass
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
