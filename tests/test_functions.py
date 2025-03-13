from pytest import raises

try:
    from typing import Any
except ImportError:
    pass

from udataclasses import (
    MISSING,
    asdict,
    dataclass,
    field,
    fields,
    is_dataclass,
    replace,
)


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


def test_asdict_nondataclass() -> None:
    with raises(TypeError):
        asdict(3)


def test_asdict_flat() -> None:
    @dataclass
    class Class:
        a: int = field()
        b: int = 2

    assert asdict(Class(a=1)) == {"a": 1, "b": 2}


def test_asdict_nested_dataclass() -> None:
    @dataclass
    class Class:
        value: int = field()
        child: Any = None

    assert asdict(Class(value=1, child=Class(value=2))) == {
        "value": 1,
        "child": {"value": 2, "child": None},
    }


def test_asdict_nested_list() -> None:
    @dataclass
    class Class:
        value: int = field()
        children: list["Class"] = field(default_factory=list)

    assert asdict(Class(value=1, children=[Class(value=2), Class(value=3)])) == {
        "value": 1,
        "children": [{"value": 2, "children": []}, {"value": 3, "children": []}],
    }


def test_asdict_nested_tuple() -> None:
    @dataclass
    class Class:
        value: int = field()
        children: tuple["Class", "Class"] | None = None

    assert asdict(Class(value=1, children=(Class(value=2), Class(value=3)))) == {
        "value": 1,
        "children": ({"value": 2, "children": None}, {"value": 3, "children": None}),
    }


def test_asdict_nested_dict() -> None:
    @dataclass
    class Class:
        value: int = field()
        children: dict[str, "Class"] = field(default_factory=dict)

    assert asdict(
        Class(value=1, children={"a": Class(value=2), "b": Class(value=3)})
    ) == {
        "value": 1,
        "children": {
            "a": {"value": 2, "children": {}},
            "b": {"value": 3, "children": {}},
        },
    }


def test_asdict_custom_factory() -> None:
    @dataclass
    class Class:
        value: int = field()
        child: Any = None

    def dict_factory(args: list[tuple[str, Any]]) -> list[tuple[str, Any]]:
        def first(arg: tuple[str, Any]) -> str:
            return arg[0]

        return sorted(args, key=first)

    assert asdict(Class(value=1, child=Class(value=2)), dict_factory=dict_factory) == [
        ("child", [("child", None), ("value", 2)]),
        ("value", 1),
    ]
