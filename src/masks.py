import logging
from pathlib import Path


# Настройка логгера для модуля masks
def setup_masks_logger() -> logging.Logger:
    """Настройка логгера для модуля masks"""
    # Создаем папку для логов
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    # Создаем логгер
    logger = logging.getLogger("masks")
    logger.setLevel(logging.DEBUG)

    # Обработчик файла (перезаписываем при каждом запуске)
    file_handler = logging.FileHandler(log_dir / "masks.log", mode="w")
    file_handler.setLevel(logging.DEBUG)

    # Форматтер с меткой времени, именем модуля, уровнем и сообщением
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    file_handler.setFormatter(formatter)

    # Добавляем обработчик
    logger.addHandler(file_handler)

    return logger


# Инициализация логгера
logger = setup_masks_logger()


def get_mask_card_number(card_number: str) -> str:
    """
    Возвращает замаскированный номер банковской карты в формате:
    XXXX XX** **** XXXX

    Аргументы:
        card_number (str): Номер карты (должен состоять из 16 цифр).

    Возвращает:
        str: Замаскированный номер карты.

    Вызывает ошибку:
        ValueError: Если номер карты не состоит из 16 цифр.
    """
    logger.debug(f"Начало маскирования номера карты: {card_number}")

    try:
        # Убедимся, что номер карты состоит только из цифр
        if not card_number.isdigit() or len(card_number) != 16:
            error_msg = "Номер карты должен содержать ровно 16 цифр"
            logger.error(f"{error_msg}: {card_number}")
            raise ValueError(error_msg)

        # Формируем маску: XXXX XX** **** XXXX
        masked = f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"

        logger.info(f"Успешно замаскирован номер карты: {masked}")
        return masked

    except Exception:  # Убрали неиспользуемую переменную 'e'
        logger.exception(f"Ошибка при маскировании карты {card_number}")
        raise


def get_mask_account(account_number: str) -> str:
    """
    Возвращает маску номера счёта в формате **XXXX (последние 4 цифры),
    где X — это цифра из номера счёта.

    :param account_number: Номер счёта (строка из цифр)
    :return: Маска номера счёта
    """
    logger.debug(f"Начало маскирования номера счета: {account_number}")

    try:
        # Проверяем, что номер счёта состоит только из цифр
        if not account_number.isdigit():
            error_msg = "Номер счёта должен содержать только цифры"
            logger.error(f"{error_msg}: {account_number}")
            raise ValueError(error_msg)

        # Берём последние 4 цифры
        last_4 = account_number[-4:]

        # Формируем маску
        masked = f"**{last_4}"

        logger.info(f"Успешно замаскирован номер счета: {masked}")
        return masked

    except Exception:  # Убрали неиспользуемую переменную 'e'
        logger.exception(f"Ошибка при маскировании счета {account_number}")
        raise
