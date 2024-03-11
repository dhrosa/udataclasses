import typing
from collections.abc import Iterator
from typing import Any, TypeVar

from .field import Field, field
from .source import Source

T = TypeVar("T")


@typing.dataclass_transform(field_specifiers=(field, Field))
def dataclass(
    cls: type[T], /, *, init: bool = True, repr: bool = True, eq: bool = True
) -> type[T]:
    transform = TransformSpec(cls, init=init, repr=repr, eq=eq)
    source = Source()

    new_methods: dict[str, Any] = {}

    def add_method(lines: Iterator[str]) -> None:
        exec(source.format(lines), None, new_methods)

    if transform.init:
        add_method(source.init(transform.fields))
    if transform.repr:
        add_method(source.repr(transform.fields))
    if transform.eq:
        add_method(source.eq(transform.fields))

    for name, value in new_methods.items():
        setattr(cls, name, value)
    return cls


class TransformSpec:
    class_name: str
    init: bool
    repr: bool
    eq: bool
    fields: list[Field]

    def __init__(
        self, cls: type[T], *, init: bool = False, repr: bool = False, eq: bool = False
    ) -> None:
        self.class_name = cls.__name__
        self.init = init and ("__init__" not in cls.__dict__)
        self.repr = repr and ("__repr__" not in cls.__dict__)
        self.eq = eq and ("__eq__" not in cls.__dict__)

        self.fields = []
        for attr in cls.__dict__:
            value = getattr(cls, attr)
            field: Field
            if isinstance(value, Field):
                field = value
                field.name = attr
            else:
                # Convert implicit field to an explicit one.
                if callable(value) or attr.startswith("__"):
                    # Ignore methods and dunder attributes
                    continue
                field = Field(attr, value)

            self.fields.append(field)
