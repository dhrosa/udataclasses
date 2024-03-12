from .dataclass import dataclass, is_dataclass
from .field import Field, FrozenInstanceError, field

VERSION = "0.0.0"
"""Read and written by the ``hatch version`` command."""

__all__ = [
    "Field",
    "FrozenInstanceError",
    "VERSION",
    "dataclass",
    "field",
    "is_dataclass",
]
