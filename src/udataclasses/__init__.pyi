"""Stubs to make type checkers understand udataclasses in a similar way it understands dataclasses.

Inspired by: https://github.com/python/typeshed/blob/main/stdlib/dataclasses.pyi#L36-L44
"""

from collections.abc import Callable
from typing import Any, Generic, TypeVar, dataclass_transform, overload

from .constants import MISSING
from .field import Field, FrozenInstanceError
from .functions import astuple, fields, is_dataclass, make_dataclass, replace

T = TypeVar("T")
R = TypeVar("R")

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

@overload
def dataclass(cls: type[T]) -> type[T]: ...
@overload
def dataclass(cls: None) -> type[T]: ...
@dataclass_transform(
    field_specifiers=(field, Field),
    # All fields are keyword-only because we don't preserve the user's field
    # ordering.
    kw_only_default=True,
)
@overload
def dataclass(
    *,
    init: bool = ...,
    repr: bool = ...,
    eq: bool = ...,
    order: bool = ...,
    unsafe_hash: bool = ...,
    frozen: bool = ...,
) -> Callable[[type[T]], type[T]]: ...

# Overload that infers type from ``default``
@overload
def field(
    *,
    default: T,
    init: bool = ...,
    repr: bool = ...,
    hash: bool | None = ...,
    compare: bool = ...,
) -> T: ...

# Overload that infers type from ``default_factory``
@overload
def field(
    *,
    default_factory: Callable[[], T],
    init: bool = ...,
    repr: bool = ...,
    hash: bool | None = ...,
    compare: bool = ...,
) -> T: ...

# Overload with no default specified in any way.
@overload
def field(
    *,
    init: bool = ...,
    repr: bool = ...,
    hash: bool | None = ...,
    compare: bool = ...,
) -> Any: ...

# Overload with no `dict_factory` specified, which returns a simple dict.
@overload
def asdict(obj: T) -> dict[str, Any]: ...

# Generic overload with custom `dict_factory`.
@overload
def asdict(obj: T, *, dict_factory: Callable[[list[tuple[str, Any]]], R]) -> R: ...
