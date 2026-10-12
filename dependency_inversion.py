"""DIP: сервіс сповіщень залежить від абстракції, а не Email чи SMS."""
from abc import ABC, abstractmethod


class MessageSender(ABC):
    # Абстракція описує потребу бізнес-сервісу, не деталі конкретного каналу.
    @abstractmethod
    def send(self, recipient, message):
        pass


class NotificationService:
    def __init__(self, sender: MessageSender):
        # Реалізація передається ззовні; тут не створюється EmailSender().
        self._sender = sender

    def notify(self, recipient, message):
        return self._sender.send(recipient, message)


class EmailSender(MessageSender):
    def send(self, recipient, message):
        # Лише імітація: справжній лист не надсилається.
        return f"Email для {recipient}: {message}"


class SmsSender(MessageSender):
    def send(self, recipient, message):
        # Лише імітація: справжня SMS не надсилається.
        return f"SMS для {recipient}: {message}"


def main():
    email_service = NotificationService(EmailSender())
    sms_service = NotificationService(SmsSender())
    print(email_service.notify("vlad@example.com", "Замовлення готове"))
    print(sms_service.notify("+380000000000", "Замовлення готове"))


if __name__ == "__main__":
    main()
