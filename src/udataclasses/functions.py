"""Module-level dataclasses functions."""

from .constants import FIELDS_NAME
from .field import Field

try:
    from typing import Any, TypeVar

    T = TypeVar("T")
except ImportError:
    pass


def is_dataclass(obj: object) -> bool:
    """Check if an object or class is a dataclass."""
    cls = obj if isinstance(obj, type) else type(obj)
    return hasattr(cls, FIELDS_NAME)


def fields(obj: object) -> tuple[Field, ...]:
    """Retrieve all the Fields of an object or class."""
    cls = obj if isinstance(obj, type) else type(obj)
    return tuple(getattr(cls, FIELDS_NAME).values())


def replace(obj: T, **changes: Any) -> T:
    """Create a new object with the specified fields replaced."""
    fields = getattr(obj, FIELDS_NAME)
    init_args = {f.name: getattr(obj, f.name) for f in fields.values() if f.init}
    for name, new_value in changes.items():
        field = fields.get(name)
        if not field:
            raise TypeError(f"Unknown field: {name}")
        if not field.init:
            raise ValueError(f"Cannot replace field defined with init=False: {name}")
        init_args[name] = new_value
    return (type(obj))(**init_args)


def asdict(
    obj: object,
    *,
    dict_factory: Any = dict,
) -> Any:
    """Convert dataclass instance to a dict."""
    if not is_dataclass(obj):
        raise TypeError(f"Expected a dataclass, got an object of type {type(obj)}")
    args: list[tuple[str, Any]] = []
    for field in fields(obj):
        name = field.name
        value = getattr(obj, name)
        args.append((name, asdict_value(value, dict_factory)))
    return dict_factory(args)


def asdict_value(obj: object, dict_factory: Any) -> Any:
    """Internal helper for asdict.

    Converts obj into a for storing into asdict entries, recursing to find
    nested dataclass instances as needed."""

    # Types that can simply be copied over without recursion.
    simple_types = {int, float, bool, complex, bytes, str, type(None)}
    if type(obj) in simple_types:
        return obj
    if is_dataclass(obj):
        return asdict(obj, dict_factory=dict_factory)
    if isinstance(obj, (list, tuple)):
        return (type(obj))(asdict_value(item, dict_factory) for item in obj)
    if isinstance(obj, dict):
        return {
            asdict_value(key, dict_factory): asdict_value(value, dict_factory)
            for key, value in obj.items()
        }
    raise TypeError(f"Unsupported type: {type(obj)}")
