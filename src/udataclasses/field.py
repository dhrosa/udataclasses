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


FACTORY_SENTINEL = object()


def field(
    *,
    default: Any = MISSING,
    default_factory: Callable[[], Any] | MissingType = MISSING,
    init: bool = True,
    repr: bool = True,
    hash: bool | None = None,
    compare: bool = True,
) -> "Field":
    """Function for explicitly declaring a field."""
    return Field(
        default=default,
        default_factory=default_factory,
        init=init,
        repr=repr,
        hash=hash,
        compare=compare,
    )


class Field:
    """
    Internal representation of a field provided by introspection routines.
    Users should not directly instantiate this class.
    """

    name: str
    default: Any
    default_factory: Callable[[], Any] | MissingType
    init: bool
    repr: bool
    hash: bool
    compare: bool

    def __init__(
        self,
        name: str = "<UNSET>",
        default: Any = MISSING,
        default_factory: Callable[[], Any] | MissingType = MISSING,
        init: bool = True,
        repr: bool = True,
        hash: bool | None = None,
        compare: bool = True,
    ) -> None:
        self.name = name
        self.default = default
        self.default_factory = default_factory
        self.init = init
        self.repr = repr
        if hash is None:
            hash = compare
        self.hash = hash
        self.compare = compare

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
