# test_generators.py
import pytest
from src.generators import filter_by_currency, transaction_descriptions, card_number_generator

# Фикстура с тестовыми данными
@pytest.fixture
def sample_transactions():
    return [
        {
            "id": 939719570,
            "operationAmount": {
                "amount": "9824.07",
                "currency": {"code": "USD"}
            },
            "description": "Перевод организации"
        },
        {
            "id": 142264268,
            "operationAmount": {
                "amount": "79114.93",
                "currency": {"code": "USD"}
            },
            "description": "Перевод со счета на счет"
        },
        {
            "id": 873106923,
            "operationAmount": {
                "amount": "43318.34",
                "currency": {"code": "RUB"}
            },
            "description": "Перевод со счета на счет"
        }
    ]

# Тесты для filter_by_currency
def test_filter_by_currency(sample_transactions):
    usd_transactions = filter_by_currency(sample_transactions, "USD")
    result = list(usd_transactions)
    assert len(result) == 2
    assert all(t["operationAmount"]["currency"]["code"] == "USD" for t in result)

def test_filter_empty_list():
    assert list(filter_by_currency([], "USD")) == []

def test_filter_no_match(sample_transactions):
    assert list(filter_by_currency(sample_transactions, "EUR")) == []

# Тесты для transaction_descriptions
def test_transaction_descriptions(sample_transactions):
    gen = transaction_descriptions(sample_transactions)
    assert next(gen) == "Перевод организации"
    assert next(gen) == "Перевод со счета на счет"
    assert next(gen) == "Перевод со счета на счет"
    with pytest.raises(StopIteration):
        next(gen)

def test_descriptions_empty_list():
    assert list(transaction_descriptions([])) == []

# Тесты для card_number_generator
@pytest.mark.parametrize("start, end, expected", [
    (1, 1, ["0000 0000 0000 0001"]),
    (1, 3, [
        "0000 0000 0000 0001",
        "0000 0000 0000 0002",
        "0000 0000 0000 0003"
    ]),
    (9999999999999999, 9999999999999999, ["9999 9999 9999 9999"])
])
def test_card_number_generator(start, end, expected):
    assert list(card_number_generator(start, end)) == expected

def test_card_formatting():
    card = next(card_number_generator(123, 123))
    assert card == "0000 0000 0000 0123"