from . import source
from .constants import FACTORY_SENTINEL, FIELDS_NAME, MISSING
from .field import FrozenInstanceError
from .transform_spec import TransformSpec

try:
    from collections.abc import Callable
    from typing import Any, TypeVar

    T = TypeVar("T")
except ImportError:
    pass


def dataclass(
    cls: type[T] | None = None, **kwargs: Any
) -> type[T] | Callable[[type[T]], type[T]]:
    """Decorator to transform a normal class into a dataclass."""

    def wrapper(cls: type[T]) -> type[T]:
        return _dataclass(cls, **kwargs)

    if cls is None:
        # Decorator called with no arguments
        return wrapper

    # Decorator called with arguments
    return wrapper(cls)


def _dataclass(
    cls: type[T],
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
    setattr(cls, FIELDS_NAME, {f.name: f for f in transform.fields})
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
        add_method(source.deleter(field, transform.frozen))

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
