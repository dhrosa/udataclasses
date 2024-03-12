from collections.abc import Callable
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


class FactorySentinelType:
    pass


FACTORY_SENTINEL = FactorySentinelType


def field(
    *,
    default: Any = MISSING,
    default_factory: Callable[[], Any] | MissingType = MISSING,
    init: bool = True,
    repr: bool = True,
    hash: Any = None,
    compare: bool = True,
    metadata: Any = None,
    kw_only: Any = MISSING,
) -> "Field":
    """Function for explicitly declaring a field."""
    return Field(default=default, default_factory=default_factory, init=init)


class Field:
    """
    Internal representation of a field provided by introspection routines.
    Users should not directly instantiate this class.
    """

    name: str
    default: Any
    default_factory: Callable[[], Any] | MissingType
    init: bool

    def __init__(
        self,
        name: str = "<UNSET>",
        default: Any = MISSING,
        default_factory: Callable[[], Any] | MissingType = MISSING,
        init: bool = True,
    ) -> None:
        self.name = name
        self.default = default
        self.default_factory = default_factory
        self.init = init

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
