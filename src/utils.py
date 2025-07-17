import json
import os


def load_json_data(file_path: str) -> list[dict]:
    """
    Загружает данные из JSON-файла и возвращает список словарей.
    Возвращает пустой список, если:
    - Файл не найден
    - Файл пустой
    - Содержимое не является списком
    """
    if not os.path.exists(file_path):
        return []

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        return []