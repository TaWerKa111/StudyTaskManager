"""
Команды для взаимодействия с данными.
"""
from abc import ABC, abstractmethod
from typing import Dict


class Command(ABC):
    """
    Интерфейс команд.

    Методы:
        - execute: выполнить команду
    """
    @abstractmethod
    def execute(self):
        pass


class AddCommand(Command):
    def __init__(self, receiver, data: Dict):
        self.receiver = receiver
        self.data = data

    def execute(self):
        self.receiver.create(self.data)


class UpdateCommand(Command):
    def __init__(self, receiver, data):
        self.receiver = receiver
        self.data = data

    def execute(self):
        if not self.receiver.update(self.data):
            raise Exception('Данные не обновлены!')


class DeleteCommand(Command):
    def __init__(self, receiver):
        self.receiver = receiver

    def execute(self):
        if not self.receiver.delete():
            raise Exception('Данные не удалены!')


class Invoker:
    def __init__(self, command):
        self.command = command

    def set_command(self, command):
        self.command = command

    def invoke(self):
        self.command.execute()


