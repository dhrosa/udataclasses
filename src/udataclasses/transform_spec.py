from .constants import FIELDS_NAME
from .field import Field


class TransformSpec:
    init: bool
    post_init: bool
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
    """Fields sorted alphabetically by name."""

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
        self.post_init = "__post_init__" in cls.__dict__
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

        fields: dict[str, Field] = {}
        # Propagate any existing fields from base class.
        fields.update(getattr(cls, FIELDS_NAME, {}))

        for name, value in cls.__dict__.items():
            field: Field
            if isinstance(value, Field):
                field = value
                field.name = name
            else:
                # Convert implicit field to an explicit one.
                if callable(value) or name.startswith("__"):
                    # Ignore methods and dunder attributes
                    continue
                field = Field(name, value)

            fields[name] = field
        self.fields = sorted(fields.values(), key=lambda f: f.name)
