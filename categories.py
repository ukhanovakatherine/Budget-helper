"""
categories.py - модуль для хранения и сортировки категорий расходов
Отвечает за:
    накопление расходов по категориям
    сортировку категорий по сумме трат с помощью сортировки вставками
"""

class CategoryTracker:
    """
    Отслеживает суммарные расходы по категориям
    totals (dict[str, float]) - словарь {категория: суммарный расход}
    """

    def __init__(self):
        """
        Инициализирует пустой трекер категорий
        """
        self.totals = {} #словарь для хранения суммарных расходов по категориям

    def add(self, category, amount):
        """
        Добавляет сумму расхода к указанной категории
        category (str) - название категории
        amount (float) - сумма расхода
        """
        self.totals[category] = self.totals.get(category, 0.0) + amount #если категория встречается впервые, то инициализируем через get

    def sorted_by_amount(self):
        """
        Возвращает список пар (категория, сумма), отсортированный по убыванию суммы
        """
        items = list(self.totals.items()) #преобразуем словарь в список пар для сортировки
        self._insertion_sort(items) #сортируем по убыванию суммы
        return items

    @staticmethod
    def _insertion_sort(items):
        """
        Сортирует список пар (категория, сумма) по убыванию суммы методом вставок
        items (list[tuple]) - список пар (название, сумма)
        """
        for i in range(1, len(items)):
            key = items[i]
            j = i - 1
            while j >= 0 and items[j][1] < key[1]:
                items[j + 1] = items[j]
                j -= 1
            items[j + 1] = key