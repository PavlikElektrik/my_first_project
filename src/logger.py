import logging
import os
from pathlib import Path


def setup_logger(name: str) -> logging.Logger:
    """Настройка логгера для модуля"""
    # Создаем папку для логов
    project_root = Path(__file__).parent.parent
    log_dir = project_root.joinpath('logs')
    log_dir.mkdir(exist_ok=True)

    # Создаем логгер
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Создаем обработчик файла
    log_file = log_dir / f"{name}.log"
    file_handler = logging.FileHandler(log_file, mode="w")
    file_handler.setLevel(logging.DEBUG)

    # Создаем форматтер
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    file_handler.setFormatter(formatter)

    # Добавляем обработчик
    logger.addHandler(file_handler)

    return logger
