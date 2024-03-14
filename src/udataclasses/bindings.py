from . import source
from .field import FACTORY_SENTINEL, MISSING, FrozenInstanceError
from .transform_spec import TransformSpec

try:
    from typing import Any
except ImportError:
    pass


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
