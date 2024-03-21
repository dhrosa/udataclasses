"""Simplified version of a pytest-like test runner for MicroPython."""

import os

try:
    from typing import Any
except ImportError:
    pass


def run_tests(path: str) -> None:
    test_globals: dict[str, Any] = {}
    with open(path, "rt") as f:
        exec(f.read(), test_globals)

    test_count = 0
    for name, test_function in test_globals.items():
        if not name.startswith("test_") or not callable(test_function):
            continue
        test_count += 1
        test_function()
    print(f"{path}: {test_count} tests passed")


def main() -> None:
    tests_dir = "tests"
    for name in os.listdir(tests_dir):
        run_tests(f"{tests_dir}/{name}")


if __name__ == "__main__":
    main()
