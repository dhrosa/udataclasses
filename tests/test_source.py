from textwrap import dedent

from udataclasses import source
from udataclasses.field import Field


def test_init() -> None:
    out = source.init([Field("a"), Field("b")])
    expected = """
    def __init__(self, a, b):
        self._a = a
        self._b = b
    """
    expected = dedent(expected).strip()
    assert out == expected


def test_getter() -> None:
    out = source.getter(Field("member"))
    expected = """
    @property
    def member(self):
        return self._member
    """
    expected = dedent(expected).strip()
    assert out == expected


def test_setter() -> None:
    out = source.setter(Field("member"))
    expected = """
    @member.setter
    def member(self, value):
        self._member = value
    """
    expected = dedent(expected).strip()
    assert out == expected


def test_repr() -> None:
    out = source.repr([Field("a"), Field("b")])
    expected = """
    def __repr__(self):
        return f'{self.__class__.__name__}(a={self._a!r}, b={self._b!r})'
    """
    expected = dedent(expected).strip()
    assert out == expected


def test_eq() -> None:
    out = source.eq([Field("a"), Field("b")])
    expected = """
    def __eq__(self, other):
        return (self._a == other._a) and (self._b == other._b)
    """
    expected = dedent(expected).strip()
    assert out == expected
