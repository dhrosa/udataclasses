from .constants import MISSING
from .decorator import dataclass
from .field import Field, FrozenInstanceError, field
from .functions import asdict, astuple, fields, is_dataclass, make_dataclass, replace

VERSION = "0.0.0"
"""Read and written by the ``hatch version`` command."""

__all__ = [
    "Field",
    "FrozenInstanceError",
    "MISSING",
    "asdict",
    "astuple",
    "dataclass",
    "field",
    "fields",
    "is_dataclass",
    "make_dataclass",
    "replace",
]
