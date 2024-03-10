from collections.abc import Iterator
from typing import Any

from .field import Field


class Source:
    """Generates source code for a dataclass."""

    indent_level: int = 0
    """Current indentation level."""

    class Indenter:
        """Context manager for automatically indenting and dedenting code."""

        def __init__(self, source: "Source") -> None:
            self.source = source

        def __enter__(self) -> None:
            self.source.indent_level += 1

        def __exit__(self, *args: Any) -> None:
            self.source.indent_level -= 1

    def indent(self) -> "Indenter":
        return Source.Indenter(self)

    def format(self, lines: Iterator[str]) -> str:
        """Indent and join output from the methods below into a single string."""

        def indented() -> Iterator[str]:
            prefix = " " * 4
            for line in lines:
                yield (prefix * self.indent_level) + line

        return "\n".join(indented())

    def init(self, fields: list[Field]) -> Iterator[str]:
        """Generates the __init__ method."""
        arg_names = ["self"] + [f.name for f in fields]
        yield f"def __init__({', '.join(arg_names)}):"
        with self.indent():
            for field in fields:
                yield f"self._{field.name} = {field.name}"

    def getter(self, field: Field) -> Iterator[str]:
        """Generates a field getter."""
        yield "@property"
        yield f"def {field.name}(self):"
        with self.indent():
            yield f"return self._{field.name}"

    def setter(self, field: Field) -> Iterator[str]:
        """Generates a field setter."""
        yield f"@{field.name}.setter"
        yield f"def {field.name}(self, value):"
        with self.indent():
            yield f"self._{field.name} = value"

    def repr(self, class_name: str, fields: list[Field]) -> Iterator[str]:
        """Generates the __repr__ method."""
        yield "def __repr__(self):"
        with self.indent():

            def parts() -> Iterator[str]:
                yield f"'{class_name}('"
                for field in fields:
                    yield f"repr(self._{field.name})"
                yield "')'"

            yield f"return {' + '.join(parts())}"

    def eq(self, fields: list[Field]) -> Iterator[str]:
        """Generates the __eq__ method."""
        yield "def __eq__(self, other):"
        with self.indent():

            def parts() -> Iterator[str]:
                for field in fields:
                    yield f"(self._{field.name} == other._{field.name})"

            yield f"return {' and '.join(parts())}"
