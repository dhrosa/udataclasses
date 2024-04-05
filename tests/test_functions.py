from pytest import raises

from udataclasses import MISSING, dataclass, field, fields, is_dataclass, replace


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


def test_replace() -> None:
    @dataclass
    class Class:
        a: int = field()
        b: int = field()

    assert replace(Class(a=1, b=2), b=3) == Class(a=1, b=3)


def test_replace_unknown_field() -> None:
    @dataclass
    class Class:
        a: int = field()
        b: int = field()

    with raises(TypeError):
        replace(Class(a=1, b=2), c=3)


def test_replace_init_false_field() -> None:
    @dataclass
    class Class:
        a: int = field()
        b: int = field(init=False)

    obj = Class(a=1)
    with raises(ValueError):
        replace(obj, b=3)
