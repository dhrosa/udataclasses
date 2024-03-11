from typing import Any


class MissingType:
    """Singleton type for MISSING value."""

    def __repr__(self) -> str:
        return "MISSING"

    def __eq__(self, other: object) -> bool:
        return other is self


MISSING = MissingType()
"""Placeholder for fields with no default value."""


class FrozenInstanceError(AttributeError):
    pass


def field(
    *,
    default: Any = MISSING,
    default_factory: Any = MISSING,
    init: bool = True,
    repr: bool = True,
    hash: Any = None,
    compare: bool = True,
    metadata: Any = None,
    kw_only: Any = MISSING,
) -> "Field":
    """Function for explicitly declaring a field."""
    return Field(default=default)


class Field:
    """
    Internal representation of a field provided by introspection routines.
    Users should not directly instantiate this class.
    """

    name: str
    default: Any

    def __init__(
        self, name: str = "<UNSET>", default: Any = MISSING, init: bool = True
    ) -> None:
        self.name = name
        self.default = default

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Field):
            return self.name == other.name
        return False

    def __repr__(self) -> str:
        return f"Field({self.name!r}, {self.default!r})"

    @property
    def _name(self) -> str:
        return f"_{self.name}"

    @property
    def default_value_name(self) -> str:
        """Name to use for storing the default value as a global."""
        return f"__dataclass_default_{self.name}"
