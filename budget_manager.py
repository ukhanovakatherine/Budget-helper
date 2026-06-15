"""
budget_manager.py - модуль, который объединяет все структуры данных в единый класс
"""

from expenses import ExpenseStorage
from categories import CategoryTracker
from stack import Stack
from tree import BinaryTree
import csv

class BudgetManager:
    """
    Хранит ежедневные расходы пользователя за месяц, отвечает на интервальные запросы, поддерживает отмену последнего расхода и ведёт дерево расходов
    storage (ExpenseStorage) - хранилище с префиксными суммами
    categories (CategoryTracker) - трекер расходов по категориям
    undo_stack (Stack) - стек для отмены последней операции
    tree (BinaryTree/None) - дерево расходов
    """

    def __init__(self, days: int):
        """
        Инициализирует бюджетный помощник на заданное число дней
        days (int) - число дней в месяце
        """
        self.storage = ExpenseStorage(days) #для хранения расходов по дням
        self.categories = CategoryTracker() #для отслеживания сумм по категориям
        self.undo_stack = Stack() #для отмены последней операции
        self.tree = None  #дерево создаётся при добавлении первого расхода

    def add_expense(self, day: int, amount: float, category: str):
        """
        Добавляет расход - обновляет хранилище, трекер категорий, стек и дерево
        day (int) - день месяца
        amount (float) - сумма расхода
        category (str) - название категории
        """
        #сохраняем расход, добавляем расход к конкретной категории, сохраняем в стек, чтобы иметь возможность отменить, и создаем дерево/сохраняем в дерево
        self.storage.add(day, amount)
        self.categories.add(category, amount)
        self.undo_stack.push((day, amount, category))
        if self.tree is None:
            self.tree = BinaryTree(day, amount, category)
        else:
            self.tree.insert(day, amount, category)

    def undo_last(self):
        """
        Отменяет последний добавленный расход
        Убирает запись из хранилища, дерева и категорий, снимает её со стека
        Возвращает tuple - (day, amount, category) - отменённая запись, IndexError - если нет операций для отмены
        """
        #мы удаляем расход с помощью стека, удаляем из дневного накопления суммы и удаляем сумму из суммы по категориям
        day, amount, category = self.undo_stack.pop()
        self.storage.daily[day - 1] -= amount
        self.storage._pref_valid = False
        self.categories.totals[category] -= amount
        #если категория стала практически нулевой, то мы удаляем категорию из словаря
        if abs(self.categories.totals[category]) < 1e-9:
            del self.categories.totals[category]
        #дерево не поддерживает удаление, поэтому пересоздаём его из актуального стека операций
        self._rebuild_tree()
        return day, amount, category

    def _rebuild_tree(self):
        """
        Пересоздаёт дерево расходов из текущего содержимого стека
        """
        #сбрасываем предыдущее дерево
        self.tree = None
        #стек хранит записи в виде списка, обходим все элементы и создаем, если оно не создано, иначе вставляем в уже существующее дерево
        for day, amount, category in self.undo_stack.get_all():
            if self.tree is None:
                self.tree = BinaryTree(day, amount, category)
            else:
                self.tree.insert(day, amount, category)

    def get_period_sum(self, start: int, end: int):
        """
        Возвращает сумму расходов за период [start, end]
        start (int) - начальный день
        end (int) - конечный день
        Возвращает float - сумма расходов
        """
        return self.storage.get_sum(start, end)

    def get_max_day(self):
        """
        Находит день с максимальным расходом (линейный поиск)
        Возвращает кортеж (day, amount)
        """
        return self.storage.find_max_day()

    def get_sorted_categories(self):
        """
        Возвращает список категорий, отсортированных по сумме трат (сортировка вставками)
        Возвращает list[tuple[str, float]] - список пар (категория, сумма) по убыванию
        """
        return self.categories.sorted_by_amount()

    def get_all_expenses(self):
        """
        Возвращает все расходы из дерева в порядке возрастания дней
        Возвращает list[tuple] - список кортежей (day, amount, category), пустой список, если дерево пустое
        """
        if self.tree is None:
            return []
        return self.tree.inorder()

    def get_expenses_by_day(self, day: int):
        """
        Возвращает все расходы за указанный день из дерева
        day (int) - номер дня
        Возвращает list[tuple[float, str]] - список (amount, category) или пустой список
        """
        if self.tree is None:
            return []
        node = self.tree.search(day) #ищем день
        if node is None:
            return []
        return node.records

    def import_from_csv(self, filename: str):
        """
        Импорт расходов из CSV файла
        filename (str) - путь к CSV файлу
        Возвращает tuple (успешно_импортировано, ошибок)
        """
        success = 0
        errors = 0
        #открываем файл с такой кодировкой, чтобы он смог обрабатывать с неправильными/нестрандартными и нечитаемыми в обычной кодировке символами
        with open(filename, 'r', encoding='utf-8-sig') as file:
            reader = csv.reader(file)
            for row_num, row in enumerate(reader, start=1):
                if not row or len(row) < 2: #пропускаем пустые строки или строки с недостаточным количеством колонок
                    errors += 1
                    continue
                try:
                    day = int(row[0].strip()) #мы извлекаем день, удаляем пробелы и преобразуем в число
                    amount = float(row[1].strip()) #извлекаем сумму и преобразуем в float, потому что у нас могут быть сотые числа
                    category = row[2].strip() if len(row) > 2 else "Прочее" #если есть категория, то записываем, если нет, то записываем ее в прочие расходы
                    self.add_expense(day, amount, category)
                    success += 1
                except Exception: #если получается ошибка при чтении строки, то добавляем в ошибки
                    errors += 1

        return success, errors