from typing import Any, Dict, List, Tuple


def filter_by_state(operations: List[Dict[str, Any]], state: str = "EXECUTED") -> List[Dict[str, Any]]:
    """
    Фильтрует список банковских операций по значению ключа 'state'.

    :param operations: Список словарей с данными о банковских операциях.
    :param state: Значение ключа 'state' для фильтрации (по умолчанию 'EXECUTED').
    :return: Новый список, содержащий только операции с указанным статусом.
    """
    return [operation for operation in operations if operation.get("state") == state]


def sort_by_date(operations: List[Dict[str, Any]], reverse: bool = True) -> List[Dict[str, Any]]:
    """
    Сортирует список операций по дате ('date').

    :param operations: Список словарей с данными о банковских операциях.
    :param reverse: Порядок сортировки (по умолчанию — убывание).
    :return: Отсортированный список словарей.
    """

    def parse_date(op: Dict[str, Any]) -> Tuple[int, int, int]:
        date_str = op["date"]  # Например: '2019-07-03T18:35:29.512364'
        date_part = date_str.split("T")[0]  # '2019-07-03'
        year, month, day = map(int, date_part.split("-"))  # (2019, 7, 3)
        return (year, month, day)

    return sorted(operations, key=parse_date, reverse=reverse)
