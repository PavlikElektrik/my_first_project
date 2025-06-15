from .masks import get_mask_account, get_mask_card_number
from datetime import datetime


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
    try:
        dt = datetime.fromisoformat(date_str)
        return dt.strftime("%d.%m.%Y")
    except ValueError:
        raise ValueError(f"Некорректный формат даты: {date_str}")
