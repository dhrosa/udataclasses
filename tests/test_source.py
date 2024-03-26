from sys import implementation

import udataclasses.source as source
from udataclasses.field import Field


def assert_lines(actual: str, expected_lines: list[str]) -> None:
    actual_lines = actual.splitlines()
    if implementation.name != "micropython":
        assert actual_lines == expected_lines
    # Manually display diff inside MicroPython
    if actual_lines == expected_lines:
        return
    print("Expected:")
    print("\n".join(expected_lines))
    print("Actual:")
    print("\n".join(actual_lines))


def test_init() -> None:
    out = source.init(
        [
            Field("a"),
            Field("b", default=2),
            Field("c", default_factory=lambda: 3),
            Field("d", init=False),
        ]
    )
    assert_lines(
        out,
        [
            "def __init__(self, *, a, b=__dataclass_default_b, c=FACTORY_SENTINEL):",
            "    self._a = a",
            "    self._b = b",
            "    self._c = __dataclass_default_c() if c is FACTORY_SENTINEL else c",
        ],
    )


def test_init_empty() -> None:
    out = source.init([])
    assert_lines(
        out,
        [
            "def __init__(self):",
            "    pass",
        ],
    )


def test_init_post_init() -> None:
    out = source.init([Field("a"), Field("b")], post_init=True)
    assert_lines(
        out,
        [
            "def __init__(self, *, a, b):",
            "    self._a = a",
            "    self._b = b",
            "    self.__post_init__()",
        ],
    )


def test_getter() -> None:
    out = source.getter(Field("member"))
    assert_lines(
        out,
        [
            "@property",
            "def member(self):",
            "    return self._member",
        ],
    )


def test_setter() -> None:
    out = source.setter(Field("member"))
    assert_lines(
        out,
        [
            "@member.setter",
            "def member(self, value):",
            "    self._member = value",
        ],
    )


def test_deleter() -> None:
    out = source.deleter(Field("member"))
    assert_lines(
        out,
        [
            "@member.deleter",
            "def member(self):",
            "    del self._member",
        ],
    )


def test_setter_frozen() -> None:
    out = source.setter(Field("member"), frozen=True)
    assert_lines(
        out,
        [
            "@member.setter",
            "def member(self, value):",
            "    raise FrozenInstanceError('member')",
        ],
    )


def test_deleter_frozen() -> None:
    out = source.deleter(Field("member"), frozen=True)
    assert_lines(
        out,
        [
            "@member.deleter",
            "def member(self):",
            "    raise FrozenInstanceError('member')",
        ],
    )


def test_repr() -> None:
    out = source.repr([Field("a"), Field("b"), Field("c", repr=False)])
    assert_lines(
        out,
        [
            "def __repr__(self):",
            "    return f'{self.__class__.__name__}(a={self._a!r}, b={self._b!r})'",
        ],
    )


def test_eq() -> None:
    out = source.eq([Field("a"), Field("b"), Field("c", compare=False)])
    assert_lines(
        out,
        [
            "def __eq__(self, other):",
            "    return (self._a, self._b,) == (other._a, other._b,)",
        ],
    )


def test_lt() -> None:
    out = source.lt([Field("a"), Field("b"), Field("c", compare=False)])
    assert_lines(
        out,
        [
            "def __lt__(self, other):",
            "    return (self._a, self._b,) < (other._a, other._b,)",
        ],
    )


def test_le() -> None:
    out = source.le([Field("a"), Field("b"), Field("c", compare=False)])
    assert_lines(
        out,
        [
            "def __le__(self, other):",
            "    return (self._a, self._b,) <= (other._a, other._b,)",
        ],
    )


def test_gt() -> None:
    out = source.gt([Field("a"), Field("b"), Field("c", compare=False)])
    assert_lines(
        out,
        [
            "def __gt__(self, other):",
            "    return (self._a, self._b,) > (other._a, other._b,)",
        ],
    )


def test_ge() -> None:
    out = source.ge([Field("a"), Field("b"), Field("c", compare=False)])
    assert_lines(
        out,
        [
            "def __ge__(self, other):",
            "    return (self._a, self._b,) >= (other._a, other._b,)",
        ],
    )


def test_hash() -> None:
    out = source.hash(
        [
            Field("a"),
            Field("b"),
            Field("c", compare=False, hash=True),
            Field("d", compare=False),
        ],
    )
    assert_lines(
        out,
        [
            "def __hash__(self):",
            "    return hash((self._a, self._b, self._c,))",
        ],
    )


def test_hash_empty() -> None:
    out = source.hash([])
    assert_lines(
        out,
        [
            "def __hash__(self):",
            "    return hash(())",
        ],
    )
