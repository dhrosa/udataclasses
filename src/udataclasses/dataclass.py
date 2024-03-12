from collections.abc import Callable
from typing import Any, TypeVar, overload

from . import source
from .field import FACTORY_SENTINEL, MISSING, Field, FrozenInstanceError
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


def is_dataclass(obj: object) -> bool:
    cls = obj if isinstance(obj, type) else type(obj)
    return hasattr(cls, FIELDS)


def fields(obj: object) -> tuple[Field, ...]:
    cls = obj if isinstance(obj, type) else type(obj)
    return tuple(getattr(cls, FIELDS).values())


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
) -> type[T]:
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


def make_global_bindings(transform: TransformSpec) -> dict[str, Any]:
    bindings: dict[str, Any] = {
        "FrozenInstanceError": FrozenInstanceError,
        "FACTORY_SENTINEL": FACTORY_SENTINEL,
    }
    for field in transform.fields:
        if field.default is not MISSING:
            bindings[field.default_value_name] = field.default
        if field.default_factory is not MISSING:
            bindings[field.default_value_name] = field.default_factory
    return bindings


def make_methods(transform: TransformSpec) -> dict[str, Any]:
    global_bindings = make_global_bindings(transform)
    methods: dict[str, Any] = {}

    def add_method(code: str) -> None:
        exec(code, global_bindings, methods)

    for field in transform.fields:
        add_method(source.getter(field))
        add_method(source.setter(field, transform.frozen))

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

    if transform.hash is None:
        methods["__hash__"] = None
    if transform.hash:
        add_method(source.hash(transform.fields))

    return methods


FIELDS = "__dataclass_fields__"
"""Class attribute used to store dataclass fields."""
