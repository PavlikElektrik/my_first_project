import pytest
from src.widget import get_date


class TestGetDate:
    """Тесты для функции форматирования даты get_date()"""

    @pytest.mark.parametrize("valid_date, expected", [
        ("2024-03-11T02:26:18.671407", "11.03.2024"),
        ("2024-03-11", "11.03.2024"),
        ("1999-12-31T23:59:59.999999", "31.12.1999")
    ])
    def test_valid_dates(self, valid_date, expected):
        """Тест корректных форматов дат"""
        assert get_date(valid_date) == expected

    @pytest.mark.parametrize("invalid_date, error_msg", [
        ("2024/03/11", "Некорректный формат даты: 2024/03/11"),
        ("", "Некорректный формат даты: "),
        ("2024-aa-11", "Некорректный формат даты: 2024-aa-11"),
        ("2024-02-30", "Некорректный формат даты: 2024-02-30"),
        ("hello_world", "Некорректный формат даты: hello_world")
    ])
    def test_invalid_dates(self, invalid_date, error_msg):
        """Тест обработки некорректных дат"""
        with pytest.raises(ValueError) as exc_info:
            get_date(invalid_date)
        assert str(exc_info.value) == error_msg
