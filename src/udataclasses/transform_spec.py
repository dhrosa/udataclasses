from typing import TypeVar

from .field import Field

T = TypeVar("T")


class TransformSpec:
    init: bool
    repr: bool
    eq: bool
    order: bool
    fields: list[Field]

    def __init__(
        self,
        cls: type[T],
        *,
        init: bool = False,
        repr: bool = False,
        eq: bool = False,
        order: bool = False,
    ) -> None:
        self.init = init and ("__init__" not in cls.__dict__)
        self.repr = repr and ("__repr__" not in cls.__dict__)
        self.eq = eq
        self.order = order

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
