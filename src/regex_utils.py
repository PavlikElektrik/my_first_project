# src/my_first_project/regex_utils.py
import re
from collections import Counter
from typing import Any, Dict, List

from src.decorators import log


@log(filename="logs/regex_utils.log")
def process_bank_search(data: List[Dict[str, Any]], search: str) -> List[Dict[str, Any]]:
    """
    Ищет в списке операций все, у которых в поле 'description'
    содержится подстрока search (регистронезависимо).
    Возвращает список найденных операций.
    """
    pattern = re.compile(re.escape(search), flags=re.IGNORECASE)
    return [op for op in data if pattern.search(str(op.get("description", "")))]


@log(filename="logs/regex_utils.log")
def process_bank_operations(data: List[Dict[str, Any]], categories: List[str]) -> Dict[str, int]:
    """
    Подсчитывает количество операций в каждой категории.

    Args:
        data (list[dict]): Список банковских операций, каждая операция — словарь с данными.
        categories (list[str]): Список категорий для подсчёта.

    Returns:
        dict[str, int]: Словарь, где ключ — категория, значение — количество операций в этой категории.
    """
    stats = {category: 0 for category in categories}  # <-- Заполняем сразу всеми ключами
    for op in data:
        description = op.get("description", "").lower()
        for category in categories:
            if category.lower() in description:
                stats[category] += 1
    return stats
