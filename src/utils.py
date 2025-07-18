import os
import json
from .logger import setup_logger

# Инициализация логгера
logger = setup_logger("utils")

def load_json_data(file_path: str) -> list[dict]:
    """
    Загружает данные из JSON-файла и возвращает список словарей.
    Возвращает пустой список, если:
    - Файл не найден
    - Файл пустой
    - Содержимое не является списком
    """
    try:
        logger.debug("Попытка загрузить файл: %s", file_path)

        if not os.path.exists(file_path):
            logger.error("Файл не найден: %s", file_path)
            return []

        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

            if not isinstance(data, list):
                logger.error("Файл %s не содержит список", file_path)
                return []

            logger.info("Успешно загружен файл: %s", file_path)
            return data

    except (json.JSONDecodeError, OSError) as e:
        logger.exception("Ошибка при загрузке файла %s: %s", file_path, str(e))
        return []
