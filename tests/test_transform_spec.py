from udataclasses.constants import MISSING
from udataclasses.field import Field, field
from udataclasses.transform_spec import TransformSpec


def test_init() -> None:
    class Empty:
        pass

    assert not TransformSpec(Empty, init=False).init
    assert TransformSpec(Empty, init=True).init

    class HasInit:
        def __init__(self) -> None:
            pass

    assert not TransformSpec(HasInit, init=False).init
    assert not TransformSpec(HasInit, init=True).init


def test_repr() -> None:
    class Empty:
        pass

    assert not TransformSpec(Empty, repr=False).repr
    assert TransformSpec(Empty, repr=True).repr

    class HasRepr:
        def __repr__(self) -> str:
            return ""

    assert not TransformSpec(HasRepr, repr=False).repr
    assert not TransformSpec(HasRepr, repr=True).repr


def test_hash() -> None:
    class Empty:
        pass

    assert TransformSpec(Empty, eq=True, frozen=True).hash is True
    assert TransformSpec(Empty, eq=False, frozen=True).hash is False
    assert TransformSpec(Empty, eq=False, frozen=False).hash is False
    assert TransformSpec(Empty, eq=True, frozen=False).hash is None

    assert TransformSpec(Empty, eq=False, frozen=False, unsafe_hash=True).hash is True


def test_fields() -> None:
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
