import pytest
from src.masks import get_mask_account, get_mask_card_number
from src.widget import get_date
from src.processing import filter_by_state, sort_by_date


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
        "1234",  # Слишком короткий
        "",  # Пустая строка
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
        "",  # Пустая строка
        "abcd1234",  # Содержит буквы
        "1234-абвг"  # Содержит спецсимволы и буквы
    ])
    def test_get_mask_account_invalid(self, invalid_account):
        """Тест обработки невалидных номеров счетов"""
        with pytest.raises(ValueError):
            get_mask_account(invalid_account)


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

    class TestFilterByState:
        """Тесты для функции filter_by_state()"""

        @pytest.fixture
        def sample_operations(self):
            return [
                {'id': 1, 'state': 'EXECUTED', 'date': '2024-01-01T00:00:00'},
                {'id': 2, 'state': 'PENDING', 'date': '2024-01-02T00:00:00'},
                {'id': 3, 'state': 'EXECUTED', 'date': '2024-01-03T00:00:00'},
                {'id': 4, 'state': 'CANCELED', 'date': '2024-01-04T00:00:00'}
            ]

        def test_filter_executed(self, sample_operations):
            """Тест фильтрации по статусу EXECUTED"""
            result = filter_by_state(sample_operations)
            assert len(result) == 2
            assert all(op['state'] == 'EXECUTED' for op in result)

        def test_filter_canceled(self, sample_operations):
            """Тест фильтрации по статусу CANCELED"""
            result = filter_by_state(sample_operations, 'CANCELED')
            assert len(result) == 1
            assert result[0]['id'] == 4

        def test_empty_input(self):
            """Тест с пустым списком операций"""
            assert filter_by_state([]) == []

    class TestSortByDate:
        """Тесты для функции sort_by_date()"""

        @pytest.fixture
        def sample_operations(self):
            return [
                {'id': 1, 'date': '2024-03-01T00:00:00'},
                {'id': 2, 'date': '2024-01-01T00:00:00'},
                {'id': 3, 'date': '2024-02-01T00:00:00'}
            ]

        def test_sort_ascending(self, sample_operations):
            """Тест сортировки по возрастанию"""
            result = sort_by_date(sample_operations, reverse=False)
            assert [op['id'] for op in result] == [2, 3, 1]

        def test_sort_descending(self, sample_operations):
            """Тест сортировки по убыванию (по умолчанию)"""
            result = sort_by_date(sample_operations)
            assert [op['id'] for op in result] == [1, 3, 2]

        def test_empty_input(self):
            """Тест с пустым списком операций"""
            assert sort_by_date([]) == []

        def test_invalid_date_format(self):
            """Тест с некорректным форматом даты"""
            with pytest.raises(ValueError):
                sort_by_date([{'date': 'invalid-date'}])


if __name__ == "__main__":
    pytest.main(["-v"])
