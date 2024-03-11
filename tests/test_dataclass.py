from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from dataclasses import dataclass, field
else:
    from udataclasses import dataclass, field


def test_repr() -> None:
    @dataclass
    class Class:
        a: int = field()
        b: int = field()

    assert repr(Class(1, 2)) == "Class(a=1, b=2)"
