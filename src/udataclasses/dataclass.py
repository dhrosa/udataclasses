from collections.abc import Callable
from typing import Any, TypeVar, overload

from . import source
from .field import FrozenInstanceError
from .transform_spec import TransformSpec

T = TypeVar("T")


# No argument and no parenthesis overload
@overload
def dataclass(cls: None, /) -> Callable[[type[T]], type[T]]:
    pass


@overload
def dataclass(cls: type[T], /) -> type[T]:
    pass


def dataclass(
    cls: type[T] | None = None, **kwargs: Any
) -> type[T] | Callable[[type[T]], type[T]]:
    def wrapper(cls: type[T]) -> type[T]:
        return _dataclass(cls, **kwargs)

    if cls is None:
        # Decorator called with no arguments
        return wrapper

    # Decorator called with arguments
    return wrapper(cls)


def _dataclass(
    cls: type[T],
    /,
    *,
    init: bool = True,
    repr: bool = True,
    eq: bool = True,
    order: bool = False,
    unsafe_hash: bool = False,
    frozen: bool = False,
    match_args: bool = True,
    kw_only: bool = False,
    slots: bool = False,
) -> type[T]:
    transform = TransformSpec(cls, init=init, repr=repr, eq=eq, order=order)

    exec_globals: dict[str, Any] = {
        "FrozenInstanceError": FrozenInstanceError,
    }
    new_methods: dict[str, Any] = {}

    def add_method(code: str) -> None:
        exec(code, exec_globals, new_methods)

    if transform.init:
        add_method(source.init(transform.fields))
    if transform.repr:
        add_method(source.repr(transform.fields))
    if transform.eq:
        add_method(source.eq(transform.fields))
    if transform.order:
        add_method(source.lt(transform.fields))
        add_method(source.le(transform.fields))
        add_method(source.gt(transform.fields))
        add_method(source.ge(transform.fields))

    for field in transform.fields:
        add_method(source.getter(field))
        add_method(source.setter(field, frozen))

    for name, value in new_methods.items():
        setattr(cls, name, value)
    return cls
