# generators.py

def filter_by_currency(transactions, currency_code):
    """Генератор для фильтрации транзакций по валюте"""
    for transaction in transactions:
        op_amount = transaction.get("operationAmount", {})
        curr_info = op_amount.get("currency", {})
        if curr_info.get("code") == currency_code:
            yield transaction

def transaction_descriptions(transactions):
    """Генератор для получения описаний транзакций"""
    for transaction in transactions:
        yield transaction["description"]

def card_number_generator(start, end):
    """Генератор номеров банковских карт в заданном диапазоне"""
    for num in range(start, end + 1):
        card_str = f"{num:016d}"
        formatted = " ".join([card_str[i:i+4] for i in range(0, 16, 4)])
        yield formatted