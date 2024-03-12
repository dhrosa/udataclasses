from typing import TYPE_CHECKING

from pytest import raises

if TYPE_CHECKING:
    from dataclasses import FrozenInstanceError, dataclass, field
else:
    from udataclasses import FrozenInstanceError, dataclass, field


def test_init_excluded_fields() -> None:
    @dataclass
    class Class:
        a: int = field()
        b: int = field(default=0, init=False)

    # mypy rightfully warns that __init__ only takes one argument
    with raises(TypeError):
        Class(1, 2)  # type: ignore

    Class(1)


def test_repr() -> None:
    @dataclass
    class Class:
        a: int = field()
        b: int = field()
        c: int = field(repr=False)

    assert repr(Class(1, 2, 3)) == "Class(a=1, b=2)"


def test_default() -> None:
    @dataclass
    class Class:
        a: int = field()
        b: int = 0

    assert Class(1) == Class(1, 0)
    assert Class(1, 2) == Class(1, 2)


def test_default_factory() -> None:
    @dataclass
    class Class:
        a: list[int] = field(default_factory=lambda: [])

    obj = Class()
    obj.a.append(1)
    assert obj.a == [1]

    obj = Class()
    assert obj.a == []


def test_properties() -> None:
    @dataclass
    class Class:
        a: int = field()

    obj = Class(1)
    assert obj.a == 1

    obj.a = 2
    assert obj.a == 2


def test_eq() -> None:
    @dataclass
    class Class:
        a: int = field()
        b: int = field()
        c: int = field(compare=False)

    assert Class(1, 2, 3) == Class(1, 2, 0)
    assert Class(1, 2, 3) != Class(1, 1, 3)


def test_compare() -> None:
    @dataclass(order=True)
    class Class:
        a: int = field()
        b: int = field()
        c: int = field(compare=False)

    assert Class(1, 2, 3) <= Class(1, 2, 0)
    assert not (Class(1, 2, 3) < Class(1, 2, 0))


def test_frozen() -> None:
    @dataclass(frozen=True)
    class Class:
        a: int = field()

    obj = Class(1)
    with raises(FrozenInstanceError):
        # Mypy rightfully warns that this assignment won't work on a frozen
        # dataclass.
        obj.a = 2  # type: ignore


def test_implicit_hash() -> None:
    @dataclass(eq=True, frozen=True)
    class Class:
        a: int = field()
        b: int = field()

    assert Class.__hash__ is not None
    assert hash(Class(1, 2)) == hash(Class(1, 2))
    assert hash(Class(1, 2)) != hash(Class(0, 2))
    assert hash(Class(1, 2)) != hash(Class(1, 1))


def test_disabled_hash() -> None:
    @dataclass(eq=True, frozen=False)
    class Class:
        a: int = field()

        def __hash__(self) -> int:
            return 4

    assert Class.__hash__ is None


def test_inherited_hash() -> None:
    @dataclass(eq=False)
    class Class:
        a: int = field()
        b: int = field()

        def __hash__(self) -> int:
            return 4

    assert Class.__hash__ is not None
    assert hash(Class(1, 2)) == 4


def test_unsafe_hash() -> None:
    @dataclass(unsafe_hash=True)
    class Class:
        a: int = field()
        b: int = field()

    assert Class.__hash__ is not None
    assert hash(Class(1, 2)) == hash(Class(1, 2))
    assert hash(Class(1, 2)) != hash(Class(0, 2))
    assert hash(Class(1, 2)) != hash(Class(1, 1))
