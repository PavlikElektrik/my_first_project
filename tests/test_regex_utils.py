import pytest

from src.regex_utils import process_bank_operations, process_bank_search

SAMPLE_DATA = [
    {"description": "Перевод клиенту", "amount": 100},
    {"description": "Открытие вклада", "amount": 200},
    {"description": "перевод в другой банк", "amount": 300},
    {"description": "оплата услуг", "amount": 400},
]


@pytest.mark.parametrize(
    "term,expected_count",
    [
        ("перевод", 2),
        ("открытие", 1),
        ("оплата", 1),
        ("неизвестно", 0),
    ],
)
def test_process_bank_search(term, expected_count):
    """
    Проверяет, что функция process_bank_search корректно фильтрует операции по ключевому слову.
    """
    result = process_bank_search(SAMPLE_DATA, term)
    assert isinstance(result, list)
    assert len(result) == expected_count


@pytest.mark.parametrize(
    "categories,expected",
    [
        (["перевод", "открытие", "оплата"], {"перевод": 2, "открытие": 1, "оплата": 1}),
        (["вклад", "услуг"], {"вклад": 1, "услуг": 1}),
        (["нет такого"], {"нет такого": 0}),
    ],
)
def test_process_bank_operations(categories, expected):
    stats = process_bank_operations(SAMPLE_DATA, categories)
    assert stats == expected
