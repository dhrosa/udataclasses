"""Module-level dataclasses functions."""

from .constants import FIELDS_NAME
from .decorator import _dataclass
from .field import Field

try:
    from typing import Any, Iterable, TypeVar

    T = TypeVar("T")
except ImportError:
    pass


def is_dataclass(obj: object) -> bool:
    """Check if an object or class is a dataclass."""
    cls = obj if isinstance(obj, type) else type(obj)
    return hasattr(cls, FIELDS_NAME)


def fields(obj: object) -> tuple[Field, ...]:
    """Retrieve all the Fields of an object or class.

    Fields are returned in alphabetical order by name.
    """
    cls = obj if isinstance(obj, type) else type(obj)
    return tuple(sorted(getattr(cls, FIELDS_NAME).values(), key=lambda f: f.name))


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


def astuple(obj: object, *, tuple_factory: Any = tuple) -> Any:
    """Intentionally unimplemented as we do not preserve field ordering."""
    raise NotImplementedError("astuple() is intentionally not implemented. ")


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


def make_dataclass(
    cls_name: str,
    fields: Iterable[str | tuple[str, Any] | tuple[str, Any, Any]],
    *,
    bases: tuple[type, ...] = (),
    namespace: dict[str, Any] | None = None,
    init: bool = True,
    repr: bool = True,
    eq: bool = True,
    order: bool = False,
    unsafe_hash: bool = False,
    frozen: bool = False,
) -> type[Any]:
    """Dynamically create a dataclass."""
    # Attributes of dynamically-created class.
    attrs = dict(**(namespace or {}))
    for f in fields:
        # Normalize fields to 3-tuple form.
        if isinstance(f, str):
            # str to 3-tuple
            f = (f, object, Field())
        if not isinstance(f, tuple):
            raise TypeError(
                f"Field specifier must be a str or tuple. Instead got {type(f)}"
            )
        if len(f) == 2:
            # 2-tuple to 3-tuple
            f = (f[0], object, Field())
        if len(f) != 3:
            raise TypeError(
                f"Field specifier must have length 2 or 3. Instead got {len(f)}"
            )
        name, _, field = f
        attrs[name] = field
    return _dataclass(
        type(cls_name, bases, attrs),
        init=init,
        repr=repr,
        eq=eq,
        order=order,
        unsafe_hash=unsafe_hash,
        frozen=frozen,
    )
