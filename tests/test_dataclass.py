from typing import TYPE_CHECKING

from pytest import raises

if TYPE_CHECKING:
    from dataclasses import FrozenInstanceError, dataclass, field
else:
    from udataclasses import FrozenInstanceError, dataclass, field


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


def test_frozen() -> None:
    @dataclass(frozen=True)
    class Class:
        a: int = field()

    obj = Class(1)
    with raises(FrozenInstanceError):
        # Mypy rightfully warns that this assignment won't work on a frozen
        # dataclass.
        obj.a = 2  # type: ignore
