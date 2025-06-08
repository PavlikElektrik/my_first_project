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
    # Убедимся, что номер карты состоит только из цифр
    if not card_number.isdigit() or len(card_number) != 16:
        raise ValueError("Номер карты должен содержать ровно 16 цифр")

    # Формируем маску: XXXX XX** **** XXXX
    masked = f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"

    return masked


def get_mask_account(account_number: str) -> str:
    """
    Возвращает маску номера счёта в формате **XXXX (последние 4 цифры),
    где X — это цифра из номера счёта.

    :param account_number: Номер счёта (строка из цифр)
    :return: Маска номера счёта
    """
    # Проверяем, что номер счёта состоит только из цифр
    if not account_number.isdigit():
        raise ValueError("Номер счёта должен содержать только цифры")

    # Берём последние 4 цифры
    last_4 = account_number[-4:]

    # Формируем маску
    masked = f"**{last_4}"

    return masked
