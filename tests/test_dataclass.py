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


def test_eq() -> None:
    @dataclass
    class Class:
        a: int = field()
        b: int = field()

    assert Class(1, 2) == Class(1, 2)
    assert Class(1, 2) != Class(1, 1)


def test_compare() -> None:
    @dataclass(order=True)
    class Class:
        a: int = field()
        b: int = field()

    assert Class(1, 2) <= Class(1, 2)
    assert not (Class(1, 2) < Class(1, 2))
