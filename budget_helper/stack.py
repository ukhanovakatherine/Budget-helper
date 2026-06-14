"""
stack.py - модуль стека для отмены последнего добавленного расхода

Реализует стек, используется для хранения истории добавленных расходов и отмены
"""


class Stack:
    """
    Стек для хранения истории операций добавления расходов
    Поддерживает добавление, просмотр верхнего элемента и удаление
    Используется для отмены последней добавленной записи расхода
    items (list) - внутренний список для хранения элементов стека
    """

    def __init__(self):
        """Инициализирует пустой стек"""
        self.items = []

    def push(self, data):
        """
        Помещает элемент на вершину стека
        data - кортеж (day, amount, category)
        """
        self.items.append(data)

    def pop(self):
        """
        Удаляет и возвращает верхний элемент стека
        Возвращает IndexError, если стек пустой
        """
        if self.is_empty():
            raise IndexError("pop from empty stack")
        return self.items.pop()

    def peek(self):
        """
        Возвращает верхний элемент стека без удаления
        Возвращает IndexError, если стек пустой
        """
        if self.is_empty():
            raise IndexError("pop from empty stack")
        return self.items[-1]

    def is_empty(self):
        """
        Проверяет, пустой ли стек
        """
        return len(self.items) == 0

    def size(self):
        """
        Возвращает количество элементов в стеке
        """
        return len(self.items)