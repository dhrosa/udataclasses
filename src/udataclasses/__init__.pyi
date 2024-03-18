# Use type annotations from original dataclasses module.

from dataclasses import (
    MISSING,
    Field,
    FrozenInstanceError,
    dataclass,
    field,
    fields,
    is_dataclass,
)

__all__ = [
    "Field",
    "FrozenInstanceError",
    "MISSING",
    "dataclass",
    "field",
    "fields",
    "is_dataclass",
]
