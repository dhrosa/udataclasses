from textwrap import dedent

from udataclasses import Field, source


def test_init() -> None:
    out = source.init([Field("a"), Field("b", default=2)])
    expected = """
    def __init__(self, a, b=2):
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


def test_setter_frozen() -> None:
    out = source.setter(Field("member"), frozen=True)
    expected = """
    @member.setter
    def member(self, value):
        raise FrozenInstanceError('member')
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


def test_lt() -> None:
    out = source.lt([Field("a"), Field("b")])
    expected = """
    def __lt__(self, other):
        return (self._a, self._b,) < (other._a, other._b,)
    """
    expected = dedent(expected).strip()
    assert out == expected


def test_le() -> None:
    out = source.le([Field("a"), Field("b")])
    expected = """
    def __le__(self, other):
        return (self._a, self._b,) <= (other._a, other._b,)
    """
    expected = dedent(expected).strip()
    assert out == expected


def test_gt() -> None:
    out = source.gt([Field("a"), Field("b")])
    expected = """
    def __gt__(self, other):
        return (self._a, self._b,) > (other._a, other._b,)
    """
    expected = dedent(expected).strip()
    assert out == expected


def test_ge() -> None:
    out = source.ge([Field("a"), Field("b")])
    expected = """
    def __ge__(self, other):
        return (self._a, self._b,) >= (other._a, other._b,)
    """
    expected = dedent(expected).strip()
    assert out == expected


def test_hash() -> None:
    out = source.hash([Field("a"), Field("b")])
    expected = """
    def __hash__(self):
        return hash((self._a, self._b,))
    """
    expected = dedent(expected).strip()
    assert out == expected
