"""OCP: нові правила знижок додаються без зміни калькулятора ціни."""
from abc import ABC, abstractmethod
from decimal import Decimal


class Discount(ABC):
    @abstractmethod
    def apply(self, amount: Decimal):
        """Для невід'ємної суми повернути ціну в межах від 0 до amount."""
        pass


class NoDiscount(Discount):
    def apply(self, amount):
        return amount


class PercentageDiscount(Discount):
    def __init__(self, percent):
        self._percent = Decimal(str(percent))
        if not self._percent.is_finite() or not 0 <= self._percent <= 100:
            raise ValueError("Знижка має бути від 0 до 100 відсотків")

    def apply(self, amount):
        return amount * (Decimal("1") - self._percent / 100)


class PriceCalculator:
    def calculate(self, amount, discount: Discount):
        value = Decimal(str(amount))
        if not value.is_finite() or value < 0:
            raise ValueError("Сума має бути скінченною і невід'ємною")
        return discount.apply(value)


# Розширення: додаємо новий клас, не редагуючи PriceCalculator.
class FixedDiscount(Discount):
    def __init__(self, value):
        self._value = Decimal(str(value))
        if not self._value.is_finite() or self._value < 0:
            raise ValueError("Знижка має бути скінченною і невід'ємною")

    def apply(self, amount):
        return max(Decimal("0"), amount - self._value)


def main():
    calculator = PriceCalculator()
    print(f"Без знижки: {calculator.calculate('1000', NoDiscount()):.2f} грн")
    print(f"Знижка 10%: {calculator.calculate('1000', PercentageDiscount(10)):.2f} грн")
    print(f"Фіксована знижка 150 грн: {calculator.calculate('1000', FixedDiscount(150)):.2f} грн")


if __name__ == "__main__":
    main()
