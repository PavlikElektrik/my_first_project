import logging
from .logger import setup_logger

# Инициализация логгера
logger = setup_logger("masks")


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
    logger.debug("Начало маскирования номера карты: %s", card_number)

    try:
        # Убедимся, что номер карты состоит только из цифр
        if not card_number.isdigit() or len(card_number) != 16:
            error_msg = "Номер карты должен содержать ровно 16 цифр"
            logger.error("%s: %s", error_msg, card_number)
            raise ValueError(error_msg)

        # Формируем маску: XXXX XX** **** XXXX
        masked = f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"

        logger.info("Успешно замаскирован номер карты: %s", masked)
        return masked

    except Exception as e:
        logger.exception("Ошибка при маскировании карты %s: %s", card_number, str(e))
        raise


def get_mask_account(account_number: str) -> str:
    """
    Возвращает маску номера счёта в формате **XXXX (последние 4 цифры),
    где X — это цифра из номера счёта.

    :param account_number: Номер счёта (строка из цифр)
    :return: Маска номера счёта
    """
    logger.debug("Начало маскирования номера счета: %s", account_number)

    try:
        # Проверяем, что номер счёта состоит только из цифр
        if not account_number.isdigit():
            error_msg = "Номер счёта должен содержать только цифры"
            logger.error("%s: %s", error_msg, account_number)
            raise ValueError(error_msg)

        # Берём последние 4 цифры
        last_4 = account_number[-4:]

        # Формируем маску
        masked = f"**{last_4}"

        logger.info("Успешно замаскирован номер счета: %s", masked)
        return masked

    except Exception as e:
        logger.exception("Ошибка при маскировании счета %s: %s", account_number, str(e))
        raise
