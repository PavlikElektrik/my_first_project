def filter_by_state(operations, state='EXECUTED'):
    """
    Фильтрует список банковских операций по значению ключа 'state'.

    :param operations: Список словарей с данными о банковских операциях.
    :param state: Значение ключа 'state' для фильтрации (по умолчанию 'EXECUTED').
    :return: Новый список, содержащий только операции с указанным статусом.
    """
    return [operation for operation in operations if operation.get('state') == state]

def sort_by_date(operations, reverse=True):
    """
    Сортирует список операций по дате ('date').

    :param operations: Список словарей с данными о банковских операциях.
    :param reverse: Порядок сортировки (по умолчанию — убывание).
    :return: Отсортированный список словарей.
    """

    # Извлекаем и парсим дату напрямую из строки в ISO-формате
    def parse_date(op):
        date_str = op['date']  # Например: '2019-07-03T18:35:29.512364'
        date_part = date_str.split('T')[0]  # '2019-07-03'
        year, month, day = map(int, date_part.split('-'))  # (2019, 7, 3)
        return (year, month, day)

    # Сортируем по ключу
    return sorted(operations, key=parse_date, reverse=reverse)
