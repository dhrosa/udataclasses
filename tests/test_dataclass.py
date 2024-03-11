from udataclasses.dataclass import dataclass


def test_repr() -> None:
    @dataclass
    class Class:
        a: int = 1
        b: int = 2

    assert repr(Class(1, 2)) == "Class(a=1, b=2)"
