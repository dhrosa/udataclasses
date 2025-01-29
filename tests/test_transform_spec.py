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


def test_post_init() -> None:
    class Empty:
        pass

    assert not TransformSpec(Empty).post_init

    class HasPostInit:
        def __post_init__(self) -> None:
            pass

    assert TransformSpec(HasPostInit).post_init


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

    assert TransformSpec(Empty, eq=True, frozen=True).hash
    assert not TransformSpec(Empty, eq=False, frozen=True).hash
    assert not TransformSpec(Empty, eq=False, frozen=False).hash
    assert TransformSpec(Empty, eq=True, frozen=False).hash is None

    assert TransformSpec(Empty, eq=False, frozen=False, unsafe_hash=True).hash


def test_field_defaults() -> None:
    class Class:
        a_missing = field()
        b_implicit: int = 1
        c_explicit = field(default=2)

        def method(self) -> None:
            pass

    # Note: field names are sorted alphabetically.
    assert TransformSpec(Class).fields == [
        Field("a_missing", MISSING),
        Field("b_implicit", 1),
        Field("c_explicit", 2),
    ]


def test_fields_sorted_alphabetically() -> None:
    class Class:
        c: int = 0
        a: int = 0
        b: int = 0

    assert TransformSpec(Class).fields == [Field("a"), Field("b"), Field("c")]


def test_fields_non_field_attributes_excluded() -> None:
    class Class:
        @staticmethod
        def smethod() -> int:
            return 0

        @classmethod
        def cmethod(cls) -> int:
            return 1

        @property
        def prop(self) -> int:
            return 2

    assert TransformSpec(Class).fields == []
