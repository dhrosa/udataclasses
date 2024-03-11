import typing
from typing import Any, TypeVar

from . import source
from .field import Field, field
from .transform_spec import TransformSpec

T = TypeVar("T")


@typing.dataclass_transform(field_specifiers=(field, Field))
def dataclass(
    cls: type[T], /, *, init: bool = True, repr: bool = True, eq: bool = True
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
