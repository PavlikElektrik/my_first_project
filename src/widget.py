from .masks import get_mask_account, get_mask_card_number


def mask_account_card(card_or_account_info: str) -> str:
    """
    Возвращает строку с замаскированным номером карты или счёта.

    Если информация начинается с 'Счет', используется маска для счёта (**XXXX).
    Во всех остальных случаях предполагается номер карты (формат XXXX XX** **** XXXX).

    :param card_or_account_info: Строка с информацией о карте или счёте
    :return: Строка с замаскированным номером
    """

    # Определяем, является ли запись счётом
    if card_or_account_info.startswith("Счет"):
        # Выделяем номер счёта (все цифры после слова "Счет")
        account_number = "".join(filter(str.isdigit, card_or_account_info[4:]))
        masked_number = get_mask_account(account_number)
        return f"Счет {masked_number}"
    else:
        # Предполагаем, что это карта — выделяем все цифры из строки
        card_number = "".join(filter(str.isdigit, card_or_account_info))
        masked_number = get_mask_card_number(card_number)

        # Возвращаем маску вместе с названием карты (до цифр)
        card_name = "".join(ch for ch in card_or_account_info if not ch.isdigit()).strip()
        return f"{card_name} {masked_number}"


def get_date(date_str: str) -> str:
    """
    Преобразует строку с датой в формате "ГГГГ-ММ-ДДTHH:MM:SS.ffffff" в строку формата "ДД.ММ.ГГГГ".

    Args:
        date_str (str): Дата и время в формате ISO (например, "2024-03-11T02:26:18.671407").

    Returns:
        str: Дата в формате "ДД.ММ.ГГГГ" (например, "11.03.2024").

    Example:
        >>> get_date("2024-03-11T02:26:18.671407")
        '11.03.2024'
    """
    # Разделяем строку на дату и время по символу 'T'
    date_part = date_str.split('T')[0]

    # Разделяем год, месяц и день
    year, month, day = date_part.split('-')

    # Форматируем в "ДД.ММ.ГГГГ"
    return f"{day}.{month}.{year}"
