from typing import Any, TypeVar

from . import source
from .transform_spec import TransformSpec

T = TypeVar("T")


def dataclass(
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
    transform = TransformSpec(cls, init=init, repr=repr, eq=eq)

    new_methods: dict[str, Any] = {}

    def add_method(code: str) -> None:
        exec(code, None, new_methods)

    if transform.init:
        add_method(source.init(transform.fields))
    if transform.repr:
        add_method(source.repr(transform.fields))
    if transform.eq:
        add_method(source.eq(transform.fields))

    for name, value in new_methods.items():
        setattr(cls, name, value)
    return cls
