"""Minimal shim to allow our pytest code to run inside MicroPython."""

try:
    from typing import Any
except ImportError:
    pass


class raises:
    def __init__(self, expected: type[Exception]):
        self.expected = expected

    def __enter__(self) -> None:
        pass

    def __exit__(self, exception_type: type[Exception] | None, *args: Any) -> bool:
        if exception_type is None:
            raise AssertionError(
                f"Expected exception was {self.expected}, but no exception raised."
            )
        # Suppress exception if it matches expectation, pass it through otherwise.
        return issubclass(self.expected, exception_type)
