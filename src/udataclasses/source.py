from .constants import MISSING
from .field import Field


def init(fields: list[Field], post_init: bool = False) -> str:
    """Generates the __init__ method."""
    init_fields = [f for f in fields if f.init]
    args: list[str] = []
    for field in init_fields:
        arg = field.name
        if field.default is not MISSING:
            arg += f"={field.default_value_name}"
        if field.default_factory is not MISSING:
            arg += "=FACTORY_SENTINEL"
        args.append(arg)

    # Force all arguments to be keyword-only. Positional arguments are confusing
    # in our use case because we don't preserve the user's field ordering.
    if args:
        args.insert(0, "*")

    body: list[str] = []
    for f in init_fields:
        value = f.name
        if f.default_factory is not MISSING:
            value = f"{f.default_value_name}() if {f.name} is FACTORY_SENTINEL else {f.name}"
        body.append(f"self.{f._name} = {value}")

    if post_init:
        body.append("self.__post_init__()")

    return method(
        name="__init__",
        non_self_args=args,
        body=body or "pass",
    )


def getter(field: Field) -> str:
    """Generates a field getter."""
    return method(
        decorator="@property",
        name=field.name,
        body=f"return self.{field._name}",
    )


def setter(field: Field, frozen: bool = False) -> str:
    """Generates a field setter."""
    return method(
        decorator=f"@{field.name}.setter",
        name=field.name,
        non_self_args=["value"],
        body=(
            f"raise FrozenInstanceError('{field.name}')"
            if frozen
            else f"self.{field._name} = value"
        ),
    )


def deleter(field: Field, frozen: bool = False) -> str:
    """Generates a field deleter."""
    return method(
        decorator=f"@{field.name}.deleter",
        name=field.name,
        body=(
            f"raise FrozenInstanceError('{field.name}')"
            if frozen
            else f"del self.{field._name}"
        ),
    )


def repr(fields: list[Field]) -> str:
    """Generates the __repr__ method."""
    return method(
        name="__repr__",
        body=(
            "return f'{self.__class__.__name__}("
            + ", ".join(f"{f.name}={{self.{f._name}!r}}" for f in fields if f.repr)
            + ")'"
        ),
    )


def eq(fields: list[Field]) -> str:
    return compare("__eq__", "==", fields)


def lt(fields: list[Field]) -> str:
    return compare("__lt__", "<", fields)


def le(fields: list[Field]) -> str:
    return compare("__le__", "<=", fields)


def gt(fields: list[Field]) -> str:
    return compare("__gt__", ">", fields)


def ge(fields: list[Field]) -> str:
    return compare("__ge__", ">=", fields)


def hash(fields: list[Field]) -> str:
    hash_fields = [f for f in fields if f.contributes_to_hash]
    return method(
        name="__hash__", body=f"return hash({tuple_str('self', hash_fields)})"
    )


# Internal helpers below


def method(
    *,
    name: str,
    body: str | list[str],
    decorator: str | None = None,
    non_self_args: list[str] = [],
) -> str:
    """Generates code for a Python method."""
    lines: list[str] = []
    if decorator is not None:
        lines.append(decorator)
    lines.append(f"def {name}({', '.join(['self'] + non_self_args)}):")
    if isinstance(body, str):
        body = [body]
    indent = " " * 4
    for line in body:
        lines.append(indent + line)
    return "\n".join(lines)


def tuple_str(object_name: str, fields: list[Field]) -> str:
    """An expressing that represents a dataclass instance as a tuple of its fields."""
    parts = (f"{object_name}._{f.name}," for f in fields)
    return f"({' '.join(parts)})"


def compare(name: str, operator: str, fields: list[Field]) -> str:
    """Generates a comparison operator method."""
    compare_fields = [f for f in fields if f.compare]
    left = tuple_str("self", compare_fields)
    right = tuple_str("other", compare_fields)
    return method(
        name=name,
        non_self_args=["other"],
        body=f"return {left} {operator} {right}",
    )
