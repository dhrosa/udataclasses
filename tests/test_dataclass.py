from pytest import raises

from udataclasses import (
    MISSING,
    FrozenInstanceError,
    dataclass,
    field,
    fields,
    is_dataclass,
)


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

    with raises(TypeError):
        # mypy rightfully warns that __init__ only takes one argument
        Class(a=1, b=2)  # type: ignore

    Class(a=1)


def test_init_is_keyword_only() -> None:
    @dataclass
    class Class:
        a: int = field()
        b: int = field()

    with raises(TypeError):
        # mypy rightfully warns that __init__ does not take positional arguments
        Class(1, 2)  # type: ignore

    Class(a=1, b=2)


def test_init_calls_post_init() -> None:
    a_value: int | None = None

    @dataclass
    class Class:
        a: int = field()

        def __post_init__(self) -> None:
            nonlocal a_value
            a_value = self.a

    Class(a=1)
    assert a_value == 1


def test_repr() -> None:
    @dataclass
    class Class:
        a: int = field()
        b: int = field()
        c: int = field(repr=False)

    assert repr(Class(a=1, b=2, c=3)) == "Class(a=1, b=2)"


def test_default() -> None:
    @dataclass
    class Class:
        a: int = field()
        b: int = 0

    assert Class(a=1) == Class(a=1, b=0)
    assert Class(a=1, b=2) == Class(a=1, b=2)


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

    obj = Class(a=1)
    assert obj.a == 1

    obj.a = 2
    assert obj.a == 2


def test_eq() -> None:
    @dataclass
    class Class:
        a: int = field()
        b: int = field()
        c: int = field(compare=False)

    assert Class(a=1, b=2, c=3) == Class(a=1, b=2, c=0)
    assert Class(a=1, b=2, c=3) != Class(a=1, b=1, c=3)


def test_compare() -> None:
    @dataclass(order=True)
    class Class:
        a: int = field()
        b: int = field()
        c: int = field(compare=False)

    assert Class(a=1, b=2, c=3) <= Class(a=1, b=2, c=0)
    assert not (Class(a=1, b=2, c=3) < Class(a=1, b=2, c=0))


def test_frozen() -> None:
    @dataclass(frozen=True)
    class Class:
        a: int = field()

    obj = Class(a=1)
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
    assert hash(Class(a=1, b=2)) == hash(Class(a=1, b=2))
    assert hash(Class(a=1, b=2)) != hash(Class(a=0, b=2))
    assert hash(Class(a=1, b=2)) != hash(Class(a=1, b=1))


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
    assert hash(Class(a=1, b=2)) == 4


def test_unsafe_hash() -> None:
    @dataclass(unsafe_hash=True)
    class Class:
        a: int = field()
        b: int = field()

    assert Class.__hash__ is not None
    assert hash(Class(a=1, b=2)) == hash(Class(a=1, b=2))
    assert hash(Class(a=1, b=2)) != hash(Class(a=0, b=2))
    assert hash(Class(a=1, b=2)) != hash(Class(a=1, b=1))


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

    instance_fields = fields(Class(a=1, b=2))
    assert len(instance_fields) == 2
    assert instance_fields[0].name == "a"
    assert instance_fields[0].default == MISSING
    assert instance_fields[1].name == "b"
    assert instance_fields[1].default == 1
