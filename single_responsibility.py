"""SRP: обчислення рахунку, його оформлення і збереження розділені."""
from dataclasses import dataclass
from decimal import Decimal
import json
from pathlib import Path
from tempfile import TemporaryDirectory


@dataclass(frozen=True)
class InvoiceItem:
    name: str
    quantity: int
    unit_price: Decimal

    def __post_init__(self):
        if self.quantity < 0 or not isinstance(self.quantity, int):
            raise ValueError("Кількість має бути цілим невід'ємним числом")
        if not self.unit_price.is_finite() or self.unit_price < 0:
            raise ValueError("Ціна має бути скінченною і невід'ємною")


@dataclass(frozen=True)
class Invoice:
    customer: str
    items: tuple

    def total(self):
        # Відповідальність: дані та правила розрахунку рахунку.
        return sum((item.quantity * item.unit_price for item in self.items), Decimal("0"))


class InvoiceFormatter:
    # Відповідальність: текстове представлення для користувача.
    def format(self, invoice: Invoice):
        lines = [f"Рахунок для: {invoice.customer}"]
        for item in invoice.items:
            lines.append(f"{item.name}: {item.quantity} x {item.unit_price:.2f} грн")
        lines.append(f"Разом: {invoice.total():.2f} грн")
        return "\n".join(lines)


class JsonInvoiceStorage:
    # Відповідальність: формат і механізм збереження даних.
    def save(self, invoice: Invoice, path):
        data = {
            "customer": invoice.customer,
            "items": [
                {"name": item.name, "quantity": item.quantity, "unit_price": str(item.unit_price)}
                for item in invoice.items
            ],
        }
        Path(path).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def main():
    invoice = Invoice("Влад", (
        InvoiceItem("Зошит", 2, Decimal("50.00")),
        InvoiceItem("Ручка", 1, Decimal("30.00")),
    ))
    print(InvoiceFormatter().format(invoice))
    # Демонстрація збереження не залишає зайвих файлів на комп'ютері.
    with TemporaryDirectory() as folder:
        path = Path(folder) / "invoice.json"
        JsonInvoiceStorage().save(invoice, path)
        print(f"Рахунок збережено у тимчасовий файл: {path.name}")


if __name__ == "__main__":
    main()
