import pytest
from src.masks import get_mask_account, get_mask_card_number
from src.widget import get_date


class TestMasks:
    """Тесты для функций маскирования карт и счетов"""

    @pytest.mark.parametrize("card_number, expected", [
        ("1234567890123456", "1234 56** **** 3456"),
        ("9876123456789012", "9876 12** **** 9012"),
        ("0000111122223333", "0000 11** **** 3333")
    ])
    def test_get_mask_card_number_valid(self, card_number, expected):
        """Тест корректного маскирования номера карты"""
        assert get_mask_card_number(card_number) == expected

    @pytest.mark.parametrize("invalid_card", [
        "1234",       # Слишком короткий
        "",           # Пустая строка
        "123456789012345",  # Не 16 цифр
        "1234abcd5678efgh"  # Содержит буквы
    ])
    def test_get_mask_card_number_invalid(self, invalid_card):
        """Тест обработки невалидных номеров карт"""
        with pytest.raises(ValueError):
            get_mask_card_number(invalid_card)

    @pytest.mark.parametrize("account, expected", [
        ("12345678901234567890", "**7890"),
        ("1234", "**1234"),
        ("000000009999", "**9999")
    ])
    def test_get_mask_account_valid(self, account, expected):
        """Тест корректного маскирования номера счёта"""
        assert get_mask_account(account) == expected

    @pytest.mark.parametrize("invalid_account", [
        "",           # Пустая строка
        "abcd1234",   # Содержит буквы
        "1234-абвг"   # Содержит спецсимволы и буквы
    ])
    def test_get_mask_account_invalid(self, invalid_account):
        """Тест обработки невалидных номеров счетов"""
        with pytest.raises(ValueError):
            get_mask_account(invalid_account)


class TestGetDate:
    """Тесты для функции форматирования даты"""

    @pytest.mark.parametrize("date_str, expected", [
        ("2024-03-11T02:26:18.671407", "11.03.2024"),
        ("2024-03-11", "11.03.2024"),
        ("1999-12-31T23:59:59.999999", "31.12.1999")
    ])
    def test_get_date_valid(self, date_str, expected):
        """Тест корректного форматирования даты"""
        assert get_date(date_str) == expected

    @pytest.mark.parametrize("invalid_date", [
        "2024/03/11",  # Неправильный разделитель
        "",            # Пустая строка
        "2024-aa-11",  # Нечисловые значения
        "2024-03",     # Неполная дата
        "2024-02-30",  # Несуществующая дата
        "hello_world"   # Полная ерунда
    ])
    def test_get_date_invalid(self, invalid_date):
        """Тест обработки невалидных дат"""
        with pytest.raises(ValueError):
            get_date(invalid_date)


if __name__ == "__main__":
    pytest.main(["-v"])