"""
expenses.py - модуль для хранения расходов и работы с префиксными суммами
Отвечает за:
    хранение ежедневных расходов в виде списка
    построение массива префиксных сумм
    ответ на запросы суммы за период O(1)
    линейный поиск дня с максимальным расходом
"""

class ExpenseStorage:
    """
    Хранит ежедневные расходы пользователя за месяц
    days (int) - количество дней в месяце
    daily (list[float]) - суммарный расход по каждому дню (индекс = день - 1)
    pref (list[float]) - массив префиксных сумм
    """

    def __init__(self, days: int = 31):
        """
        Инициализирует хранилище на заданное число дней
        days (int) - число дней в месяце (по умолчанию 31)
        """
        self.days = days
        #суммарный расход за каждый день
        self.daily = [0.00] * days
        #массив префиксных сумм, строится при первом запросе или после добавления
        self.pref = [0.00] * days
        #флаг, актуален ли массив префиксных сумм
        self._pref_valid = False

    def add(self, day: int, amount: float):
        """
        Добавляет сумму расхода к указанному дню
        day (int) - день месяца
        amount (float) - сумма расхода (должна быть положительной)
        Возвращает ValueError - если день вне допустимого диапазона или сумма <= 0
        """
        if not (1 <= day <= self.days):
            raise ValueError(f"День должен быть от 1 до {self.days}")
        if amount <= 0:
            raise ValueError(f"Сумма расхода должна быть положительной")
        self.daily[day - 1] += amount
        #после изменения данных префиксный массив нужно пересчитать
        self._pref_valid = False

    def _build_prefix(self):
        """
        Строит массив префиксных сумм по массиву daily
        Сложность: O(n), где n = self.days
        """
        self.pref[0] = self.daily[0]
        for i in range(1, self.days):
            self.pref[i] = self.pref[i - 1] + self.daily[i]
        self._pref_valid = True

    def get_sum(self, start: int, end: int):
        """
        Возвращает сумму расходов за период [start, end] включительно
        Ответ строится за O(1) с использованием массива префиксных сумм
        start (int) - начальный день периода
        end (int) - конечный день периода
        Возвращает float - сумма расходов за указанный период, ValueError - если дни вне диапазона или start > end
        """
        if not (1 <= start <= self.days) or not (1 <= end <= self.days):
            raise ValueError(f"Дни должны быть от 1 до {self.days}")
        if start > end:
            raise ValueError(f"Начало периода не может быть позже конца")

        # Пересчитываем, только если данные изменились
        if not self._pref_valid:
            self._build_prefix()

        if start == 1:
            return self.pref[end - 1]
        return self.pref[end - 1] - self.pref[start - 2]

    def find_max_day(self):
        """
        Находит день с максимальным суммарным расходом с помощью линейного поиска
        Линейный поиск применяется, так как массив daily не отсортирован
        Возвращает tuple (day, amount) - день и сумма расхода в этот день, если все расходы нулевые, возвращает (1, 0)
        """
        max_day = 0 #индекс дня с максимумом
        max_amount = self.daily[0]

        for i in range(1, self.days):
            #проходим линейно по каждому элементу и обновляем максимум
            if self.daily[i] > max_amount:
                max_amount = self.daily[i]
                max_day = i

        return max_day + 1, max_amount  #возвращаем день, а не индекс