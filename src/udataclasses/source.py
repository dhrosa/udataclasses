from collections.abc import Callable, Iterator
from typing import ParamSpec, TypeAlias

from .field import MISSING, Field


class IndentType:
    pass


indent = IndentType()

Lines: TypeAlias = Iterator[IndentType | str]

P = ParamSpec("P")


def formatted(f: Callable[P, Lines]) -> Callable[P, str]:
    def inner(*args: P.args, **kwargs: P.kwargs) -> str:
        parts: list[str] = []
        indent_level = 0
        for element in f(*args, **kwargs):
            if isinstance(element, IndentType):
                indent_level += 1
                continue
            parts.append(" " * (4 * indent_level) + element)
        return "\n".join(parts)

    return inner


@formatted
def init(fields: list[Field]) -> Lines:
    """Generates the __init__ method."""
    args = ["self"]
    for field in fields:
        arg = field.name
        if field.default is not MISSING:
            arg += f"={field.default!r}"
        args.append(arg)
    yield f"def __init__({', '.join(args)}):"
    yield indent
    for field in fields:
        yield f"self._{field.name} = {field.name}"


@formatted
def getter(field: Field) -> Lines:
    yield "@property"
    yield f"def {field.name}(self):"
    yield indent
    yield f"return self._{field.name}"


@formatted
def setter(field: Field) -> Lines:
    yield f"@{field.name}.setter"
    yield f"def {field.name}(self, value):"
    yield indent
    yield f"self._{field.name} = value"


@formatted
def repr(fields: list[Field]) -> Lines:
    """Generates the __repr__ method."""
    yield "def __repr__(self):"
    yield indent
    yield (
        "return f'{self.__class__.__name__}("
        + ", ".join(f"{f.name}={{self._{f.name}!r}}" for f in fields)
        + ")'"
    )


@formatted
def eq(fields: list[Field]) -> Lines:
    """Generates the __eq__ method."""
    yield "def __eq__(self, other):"
    yield indent
    yield "return " + " and ".join(
        f"(self._{f.name} == other._{f.name})" for f in fields
    )
