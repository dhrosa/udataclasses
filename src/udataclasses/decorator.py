from .bindings import make_methods
from .transform_spec import TransformSpec

FIELDS = "__dataclass_fields__"
"""Class attribute used to store dataclass fields."""


def dataclass(cls=None, **kwargs):
    def wrapper(cls):  # type: ignore
        return _dataclass(cls, **kwargs)

    if cls is None:
        # Decorator called with no arguments
        return wrapper

    # Decorator called with arguments
    return wrapper(cls)


def _dataclass(
    cls,
    *,
    init=True,
    repr=True,
    eq=True,
    order=False,
    unsafe_hash=False,
    frozen=False,
):
    transform = TransformSpec(
        cls,
        init=init,
        repr=repr,
        eq=eq,
        order=order,
        unsafe_hash=unsafe_hash,
        frozen=frozen,
    )

    for name, value in make_methods(transform).items():
        setattr(cls, name, value)

    # Store fields metadata
    setattr(cls, FIELDS, {f.name: f for f in transform.fields})
    return cls
