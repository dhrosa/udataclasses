from collections.abc import Callable
from typing import Any, TypeVar

T = TypeVar("T")

FIELDS: str

def dataclass(
    cls: type[T] | None = None, **kwargs: Any
) -> type[T] | Callable[[type[T]], type[T]]: ...
def _dataclass(
    cls: type[T],
    *,
    init: bool = True,
    repr: bool = True,
    eq: bool = True,
    order: bool = False,
    unsafe_hash: bool = False,
    frozen: bool = False,
) -> type[T]: ...
