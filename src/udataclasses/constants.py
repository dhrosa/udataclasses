FIELDS_NAME = "__dataclass_fields__"
"""Class attribute used to store dataclass fields."""

FACTORY_SENTINEL = object()
"""Placeholder used in generated __init__ parameters for fields with a default_factory."""

try:
    # If enum is available, use it to define MISSING so that we can use it with
    # typing.Literal. Inspired by:
    # https://github.com/python/typeshed/blob/adde7cc3ac277953d558ba42dc0fbdb2e4565326/stdlib/dataclasses.pyi#L36-L44
    import enum
    from typing import Literal, TypeAlias

    class MissingType(enum.Enum):
        MISSING = enum.auto()

    MISSING = MissingType.MISSING
    MissingLiteral: TypeAlias = Literal[MissingType.MISSING]

except ImportError:
    # Fallback to our own singleton type in environments like MicroPython

    class MissingType:  # type: ignore[no-redef]
        """Singleton type for MISSING value."""

        def __repr__(self) -> str:
            return "MISSING"

        def __eq__(self, other: object) -> bool:
            return other is self

    MISSING = MissingType()  # type: ignore[call-arg]
    """Sentinel default value for fields without a default value."""
