import pytest
from src.processing import filter_by_state


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
