"""
main.py - основная программа, которая запускает помощник и выводит поле для взаимодействия с пользователем
Все функции вынесены в отдельные модули:
    expenses.py - хранилище расходов и префиксные суммы
    categories.py - трекер и сортировка категорий
    stack.py - стек для отмены операций
    tree.py - дерево расходов
    budget_manager.py - главный модуль, который соединяет все остальные
"""

from budget_manager import BudgetManager

def print_menu():
    '''
    Выводит главное меню программы
    '''
    print("Бюджетный помощник")
    print("1. Добавить расход")
    print("2. Сумма расходов за период")
    print("3. День с максимальным расходом")
    print("4. Категории по сумме трат")
    print("5. Отменить последний расход")
    print("6. Все расходы")
    print("7. Расходы за конкретный день")
    print("0. Выход")

def input_int(prompt):
    '''
    Запрашивает у пользователя целое число
    prompt(str) - текст, который ввели
    Возвращает int - введённое число
    '''
    while True:
        try:
            return int(input(prompt).strip())
        except ValueError:
            print("Введите целое число")


def input_float(prompt):
    """
    Запрашивает у пользователя число с плавающей точкой
    prompt(str) - текст, который ввели
    Возвращает float - введённое число
    """
    while True:
        try:
            value = float(input(prompt).strip())
            return value
        except ValueError:
            print("Введите число")


def handle_add(manager: BudgetManager):
    """
    Обрабатывает добавление нового расхода
    manager (BudgetManager) - объект бюджетного помощника
    """
    print("\nДобавление расхода")
    day = input_int(f"День: ")
    amount = input_float("Сумма (руб.): ")
    category = input("Категория: ").strip()
    if not category:
        category = "Прочее"
    try:
        manager.add_expense(day, amount, category)
        print(f"Добавлено: день {day}, {amount:.2f} руб., категория «{category}»")
    except ValueError as e:
        print(f"Ошибка: {e}")


def handle_period_sum(manager: BudgetManager):
    """
    Обрабатывает запрос суммы расходов за период
    manager (BudgetManager) - объект бюджетного помощника
    """
    print("\nСумма за период")
    start = input_int("День начала: ")
    end = input_int("День конца: ")
    try:
        total = manager.get_period_sum(start, end)
        print(f"Расходы с дня {start} по день {end}: {total:.2f} руб.")
    except ValueError as e:
        print(f"Ошибка: {e}")


def handle_max_day(manager: BudgetManager):
    """
    Обрабатывает запрос дня с максимальным расходом
    manager (BudgetManager) - объект бюджетного помощника
    """
    print("\nДень с максимальным расходом")
    day, amount = manager.get_max_day()
    if amount == 0:
        print("Расходов пока нет")
    else:
        print(f"День {day}: {amount:.2f} руб.")


def handle_categories(manager: BudgetManager):
    """
    Выводит категории, отсортированные по сумме трат
    manager (BudgetManager) - объект бюджетного помощника
    """
    print("\nКатегории по сумме трат")
    items = manager.get_sorted_categories()
    if not items:
        print("Категорий пока нет")
        return
    for rank, (cat, total) in enumerate(items, start=1):
        print(f"  {rank}. {cat}: {total:.2f} руб.")


def handle_undo(manager: BudgetManager):
    """
    Обрабатывает отмену последнего добавленного расхода
    manager (BudgetManager) - объект бюджетного помощника
    """
    print("\nОтмена последнего расхода")
    try:
        day, amount, category = manager.undo_last()
        print(f"Отменено: день {day}, {amount:.2f} руб., категория «{category}»")
    except IndexError as e:
        print(f"Ошибка, {e}")


def handle_all_expenses(manager: BudgetManager):
    """
    Выводит все расходы из дерева в порядке возрастания дней
    manager (BudgetManager) - объект бюджетного помощника
    """
    print("\nВсе расходы")
    records = manager.get_all_expenses()
    if not records:
        print("Расходов пока нет.")
        return
    for day, amount, category in records:
        print(f"День {day:2d}: {amount:10.2f} руб., {category}")


def handle_day_expenses(manager: BudgetManager):
    """
    Выводит все расходы за конкретный день из дерева.
    manager (BudgetManager) - объект бюджетного помощника
    """
    print("\nРасходы за конкретный день")
    day = input_int(f"День: ")
    records = manager.get_expenses_by_day(day)
    if not records:
        print(f"Расходов за день {day} не найдено")
        return
    print(f"День {day}:")
    for amount, category in records:
        print(f"{amount:.2f} руб. - {category}")


def main():
    """
    Основная функция - запрашивает число дней и запускает меню
    """
    print("Добро пожаловать в Бюджетный помощник")
    days = input_int("Введите количество дней в месяце: ")
    if days > 31 or days < 28:
        print('Ошибка, введите корректное количество дней')
        return main()

    manager = BudgetManager(days)

    actions = {
        1: handle_add,
        2: handle_period_sum,
        3: handle_max_day,
        4: handle_categories,
        5: handle_undo,
        6: handle_all_expenses,
        7: handle_day_expenses,
    }

    while True:
        print_menu()
        choice = input_int("Ваш выбор: ")
        if choice == 0:
            print("До свидания!")
            break
        action = actions.get(choice)
        if action:
            action(manager)
        else:
            print("Неверный выбор, попробуйте ещё раз")


if __name__ == "__main__":
    main()