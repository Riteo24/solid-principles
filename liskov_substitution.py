"""LSP: будь-яку реалізацію Shape можна передати клієнту total_area()."""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from math import isfinite


class Shape(ABC):
    @abstractmethod
    def area(self):
        """Повернути невід'ємну числову площу, не змінюючи стан фігури.

        Метод не потребує додаткових аргументів або попередніх дій клієнта.
        """
        pass


def validate_dimension(value):
    if not isfinite(value) or value < 0:
        raise ValueError("Розмір має бути скінченним і невід'ємним")


@dataclass(frozen=True)
class Rectangle(Shape):
    width: float
    height: float

    def __post_init__(self):
        validate_dimension(self.width)
        validate_dimension(self.height)

    def area(self):
        return self.width * self.height


@dataclass(frozen=True)
class Square(Shape):
    side: float

    def __post_init__(self):
        validate_dimension(self.side)

    def area(self):
        return self.side * self.side


def total_area(shapes):
    # Клієнт знає лише контракт Shape.area(), а не конкретні типи.
    return sum(shape.area() for shape in shapes)


def main():
    rectangle = Rectangle(4, 5)
    square = Square(3)
    print(f"Площа прямокутника: {total_area([rectangle]):g}")
    print(f"Площа квадрата: {total_area([square]):g}")
    print(f"Загальна площа: {total_area([rectangle, square]):g}")


if __name__ == "__main__":
    main()
