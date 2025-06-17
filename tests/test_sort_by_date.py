import pytest
from src.processing import sort_by_date


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
