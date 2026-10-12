"""ISP: друк та сканування мають окремі інтерфейси для різних клієнтів."""
from abc import ABC, abstractmethod


class Printer(ABC):
    @abstractmethod
    def print_document(self, document):
        pass


class Scanner(ABC):
    @abstractmethod
    def scan_document(self):
        pass


class SimplePrinter(Printer):
    def print_document(self, document):
        return f"Звичайний принтер друкує: {document}"


class MultifunctionDevice(Printer, Scanner):
    def print_document(self, document):
        return f"Багатофункціональний пристрій друкує: {document}"

    def scan_document(self):
        return "Відсканований документ"


def print_report(printer: Printer, text):
    # Клієнт друку не залежить від методів сканування.
    return printer.print_document(text)


def scan_report(scanner: Scanner):
    # Клієнт сканування не залежить від методів друку.
    return scanner.scan_document()


def main():
    printer = SimplePrinter()
    multifunction = MultifunctionDevice()
    print(print_report(printer, "Звіт студента"))
    print(print_report(multifunction, "Звіт студента"))
    print(scan_report(multifunction))


if __name__ == "__main__":
    main()
