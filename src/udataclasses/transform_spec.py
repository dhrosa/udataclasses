from .field import Field


class TransformSpec:
    init: bool
    repr: bool
    eq: bool
    order: bool
    frozen: bool
    hash: bool | None
    """Tri-state value for adding a __hash__ method.

    If True, add a __hash__ method.
    If False, don't add a __hash__ method.
    If None, set __hash__ to None
    """

    fields: list[Field]

    def __init__(
        self,
        cls: type,
        *,
        init: bool = False,
        repr: bool = False,
        eq: bool = False,
        order: bool = False,
        unsafe_hash: bool = False,
        frozen: bool = False,
    ) -> None:
        self.init = init and ("__init__" not in cls.__dict__)
        self.repr = repr and ("__repr__" not in cls.__dict__)
        self.eq = eq
        self.order = order
        self.frozen = frozen

        self.hash = False
        if eq:
            if frozen:
                self.hash = True
            else:
                self.hash = None
        if unsafe_hash:
            self.hash = True

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
