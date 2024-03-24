from sys import implementation

from pytest import raises

from udataclasses import (
    MISSING,
    FrozenInstanceError,
    dataclass,
    field,
    fields,
    is_dataclass,
)

try:
    from collections.abc import Callable
    from typing import TypeAlias

    Test: TypeAlias = Callable[[], None]

except ImportError:
    pass


def exclude_micropython(test: Test) -> Test:
    """Decorator to exclude a test from running under MicroPython."""

    def inner() -> None:
        if implementation.name == "micropython":
            return
        test()

    return inner


def test_empty() -> None:
    @dataclass
    class Empty:
        pass

    Empty()


def test_init_excluded_fields() -> None:
    @dataclass
    class Class:
        a: int = field()
        b: int = field(default=0, init=False)

    # mypy rightfully warns that __init__ only takes one argument
    with raises(TypeError):
        Class(1, 2)  # type: ignore

    Class(1)


@exclude_micropython
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


@exclude_micropython
def test_eq() -> None:
    @dataclass
    class Class:
        a: int = field()
        b: int = field()
        c: int = field(compare=False)

    assert Class(1, 2, 3) == Class(1, 2, 0)
    assert Class(1, 2, 3) != Class(1, 1, 3)


@exclude_micropython
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
        # Mypy rightfully warns that this statement won't work on a frozen
        # dataclass.
        obj.a = 2  # type: ignore

    with raises(FrozenInstanceError):
        del obj.a


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


def test_is_dataclass() -> None:
    @dataclass
    class DataClass:
        a: int = 0

    class NormalClass:
        a: int = 0

    assert is_dataclass(DataClass)
    assert not is_dataclass(NormalClass)


def test_fields() -> None:
    @dataclass
    class Class:
        a: int = field()
        b: int = field(default=1)

    class_fields = fields(Class)
    assert len(class_fields) == 2
    assert class_fields[0].name == "a"
    assert class_fields[0].default == MISSING
    assert class_fields[1].name == "b"
    assert class_fields[1].default == 1

    instance_fields = fields(Class(1, 2))
    assert len(instance_fields) == 2
    assert instance_fields[0].name == "a"
    assert instance_fields[0].default == MISSING
    assert instance_fields[1].name == "b"
    assert instance_fields[1].default == 1
