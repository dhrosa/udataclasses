FIELDS_NAME = "__dataclass_fields__"
"""Class attribute used to store dataclass fields."""


class MissingType:
    """Singleton type for MISSING value."""

    def __repr__(self) -> str:
        return "MISSING"

    def __eq__(self, other: object) -> bool:
        return other is self


MISSING = MissingType()
"""Sentinel default value for fields without a default value."""

FACTORY_SENTINEL = object()
"""Placeholder used in generated __init__ parameters for fields with a default_factory."""
