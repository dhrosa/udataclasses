from udataclasses.dataclass import TransformSpec, dataclass
from udataclasses.field import MISSING, Field, field


def test_transform_spec_class_name() -> None:
    class Empty:
        pass

    assert TransformSpec(Empty).class_name == "Empty"


def test_transform_spec_init() -> None:
    class Empty:
        pass

    assert not TransformSpec(Empty, init=False).init
    assert TransformSpec(Empty, init=True).init

    class HasInit:
        def __init__(self) -> None:
            pass

    assert not TransformSpec(HasInit, init=False).init
    assert not TransformSpec(HasInit, init=True).init


def test_transform_spec_repr() -> None:
    class Empty:
        pass

    assert not TransformSpec(Empty, repr=False).repr
    assert TransformSpec(Empty, repr=True).repr

    class HasRepr:
        def __repr__(self) -> str:
            return ""

    assert not TransformSpec(HasRepr, repr=False).repr
    assert not TransformSpec(HasRepr, repr=True).repr


def test_transform_spec_eq() -> None:
    class Empty:
        pass

    assert not TransformSpec(Empty, eq=False).eq
    assert TransformSpec(Empty, eq=True).eq

    class HasEq:
        def __eq__(self, other: object) -> bool:
            return False

    assert not TransformSpec(HasEq, eq=False).eq
    assert not TransformSpec(HasEq, eq=True).eq


def test_transform_spec_fields() -> None:
    class Class:
        missing_default = field()
        implicit: int = 1
        explicit = field(default=2)

        def method(self) -> None:
            pass

    assert TransformSpec(Class).fields == [
        Field("missing_default", MISSING),
        Field("implicit", 1),
        Field("explicit", 2),
    ]


def test_dataclass_repr() -> None:
    @dataclass
    class Class:
        a: int = 1
        b: int = 2

    assert repr(Class(1, 2)) == "Class(a=1, b=2)"
