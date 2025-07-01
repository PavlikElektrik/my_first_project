from datetime import datetime

from .masks import get_mask_account, get_mask_card_number


def mask_account_card(card_or_account_info: str) -> str:
    # Обработка пустой строки
    if not card_or_account_info:
        return ""

    # Определяем, является ли запись счётом
    if card_or_account_info.startswith("Счет"):
        # Обработка случая, когда есть только слово "Счет"
        if len(card_or_account_info) <= 4:  # Только "Счет" без номера
            return card_or_account_info

        # Выделяем номер счёта
        rest = card_or_account_info[4:].strip()
        if not rest:  # Если после "Счет" только пробелы
            return "Счет **"

        account_number = "".join(filter(str.isdigit, rest))
        if not account_number:  # Если нет цифр
            return "Счет **"

        masked_number = get_mask_account(account_number)
        return f"Счет {masked_number}"
    else:
        # Выделяем номер карты
        card_number = "".join(filter(str.isdigit, card_or_account_info))

        # Если номер карты неполный
        if len(card_number) != 16:
            return card_or_account_info  # Возвращаем оригинал

        masked_number = get_mask_card_number(card_number)

        # ИЗМЕНЕНИЕ: Сохраняем название карты с пробелами
        # Находим последнюю нецифровую часть строки перед номером
        card_name = ""
        for char in card_or_account_info:
            if char.isdigit():
                break
            card_name += char
        card_name = card_name.strip()

        return f"{card_name} {masked_number}" if card_name else masked_number


def get_date(date_str: str) -> str:
    try:
        dt = datetime.fromisoformat(date_str)
        return dt.strftime("%d.%m.%Y")
    except ValueError:
        raise ValueError(f"Некорректный формат даты: {date_str}")
