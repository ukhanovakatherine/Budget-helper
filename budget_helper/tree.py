"""
tree.py - модуль двоичного дерева для хранения расходов

Каждый узел дерева хранит номер дня и список расходов этого дня
Дерево позволяет быстро искать расходы по дню, добавлять записи и обходить все расходы в порядке возрастания дней (in-order обход)
"""


class BinaryTree:
    """
    Узел двоичного дерева поиска для хранения расходов по дням
    Ключ узла - номер дня. В каждом узле хранится список кортежей (amount, category) - все расходы, добавленные в этот день
    key (int) - номер дня (ключ для поиска)
    records (list[tuple]) - список (amount, category) для этого дня
    left_child (BinaryTree/None) - левое поддерево
    right_child (BinaryTree/None) - правое поддерево
    """

    def __init__(self, key: int, amount: float, category: str):
        """
        Создаёт узел дерева для указанного дня с первой записью расхода
        key (int) - номер дня
        amount (float) - сумма первого расхода
        category (str) - категория первого расхода
        """
        self.key = key
        self.records = [(amount, category)] #список всех расходов этого дня в виде кортежей (сумма, категория)
        self.left_child = None
        self.right_child = None

    def insert(self, key: int, amount: float, category: str):
        """
        Вставляет запись расхода в дерево
        Если узел с таким днём уже существует, то добавляет запись в его список, если нет, то рекурсивно спускается влево (key < текущего) или вправо (key > текущего)
        key (int) - номер дня
        amount (float) - сумма расхода
        category (str) - категория расхода
        """
        if key == self.key:
            #день уже есть в дереве, поэтому добавляем запись в список
            self.records.append((amount, category))
        elif key < self.key:
            #идём в левое поддерево (меньший день)
            if self.left_child is None:
                self.left_child = BinaryTree(key, amount, category)
            else:
                self.left_child.insert(key, amount, category)
        else:
            #идём в правое поддерево (больший день)
            if self.right_child is None:
                self.right_child = BinaryTree(key, amount, category)
            else:
                self.right_child.insert(key, amount, category)

    def search(self, key: int):
        """
        Ищет узел с заданным днём
        key (int) - номер дня для поиска
        Возвращает BinaryTree/None - найденный узел или None
        """
        if key == self.key:
            return self
        elif key < self.key:
            #ищем в левом поддереве
            if self.left_child is None:
                return None
            return self.left_child.search(key)
        else:
            #ищем в правом поддереве
            if self.right_child is None:
                return None
            return self.right_child.search(key)

    def inorder(self):
        """
        Выполняет in-order (левый - корень - правый) обход дерева

        Возвращает все записи расходов в порядке возрастания дней, list[tuple] - список кортежей (day, amount, category)
        """
        result = []
        #сначала обходим левое поддерево (меньшие дни)
        if self.left_child:
            result.extend(self.left_child.inorder())
        #добавляем все записи текущего узла
        for amount, category in self.records:
            result.append((self.key, amount, category))
        #затем обходим правое поддерево (большие дни)
        if self.right_child:
            result.extend(self.right_child.inorder())
        return result

    def sum_prices(self):
        """
        Рекурсивно обходит дерево и суммирует все расходы
        Возвращает float - суммарный расход по всем узлам дерева
        """
        total = sum(amount for amount, _ in self.records)
        #суммируем левое поддерево
        if self.left_child:
            total += self.left_child.sum_prices()
        #суммируем правое поддерево
        if self.right_child:
            total += self.right_child.sum_prices()
        return total