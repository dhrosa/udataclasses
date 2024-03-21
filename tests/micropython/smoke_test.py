"""This file imports and runs some simple udataclasses code."""

from udataclasses import dataclass, field


@dataclass
class Product:
    name: str = field()
    quantity: int = field()


def main() -> None:
    Product("bolt", 3)
    Product("washer", 8)

    print("MicroPython smoke test success!")


if __name__ == "__main__":
    main()
