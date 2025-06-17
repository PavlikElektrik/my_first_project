import pytest

from src.masks import get_mask_account, get_mask_card_number


class TestMasks:
    """Тесты для функций маскирования карт и счетов"""

    @pytest.mark.parametrize(
        "card_number, expected",
        [
            ("1234567890123456", "1234 56** **** 3456"),
            ("9876123456789012", "9876 12** **** 9012"),
            ("0000111122223333", "0000 11** **** 3333"),
        ],
    )
    def test_get_mask_card_number_valid(self, card_number, expected):
        """Тест корректного маскирования номера карты"""
        assert get_mask_card_number(card_number) == expected

    @pytest.mark.parametrize(
        "invalid_card",
        [
            "1234",  # Слишком короткий
            "",  # Пустая строка
            "123456789012345",  # Не 16 цифр
            "1234abcd5678efgh",  # Содержит буквы
        ],
    )
    def test_get_mask_card_number_invalid(self, invalid_card):
        """Тест обработки невалидных номеров карт"""
        with pytest.raises(ValueError):
            get_mask_card_number(invalid_card)

    @pytest.mark.parametrize(
        "account, expected", [("12345678901234567890", "**7890"), ("1234", "**1234"), ("000000009999", "**9999")]
    )
    def test_get_mask_account_valid(self, account, expected):
        """Тест корректного маскирования номера счёта"""
        assert get_mask_account(account) == expected

    @pytest.mark.parametrize(
        "invalid_account",
        ["", "abcd1234", "1234-абвг"],  # Пустая строка  # Содержит буквы  # Содержит спецсимволы и буквы
    )
    def test_get_mask_account_invalid(self, invalid_account):
        """Тест обработки невалидных номеров счетов"""
        with pytest.raises(ValueError):
            get_mask_account(invalid_account)
