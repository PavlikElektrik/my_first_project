import os
import requests
from dotenv import load_dotenv

load_dotenv()


def convert_transaction_to_rub(transaction: dict) -> float:
    """
    Конвертирует сумму транзакции в рубли.
    Поддерживает USD и EUR через внешнее API.
    """
    amount = transaction['amount']
    currency = transaction['operationCurrency']['code']

    if currency == 'RUB':
        return float(amount)

    if currency not in ('USD', 'EUR'):
        raise ValueError(f"Неподдерживаемая валюта: {currency}")

    api_key = os.getenv('API_KEY_EXCHANGERATES')
    if not api_key:
        raise RuntimeError("API ключ не найден")

    response = requests.get(
        f"https://api.apilayer.com/exchangerates_data/latest?base={currency}&symbols=RUB",
        headers={'apikey': api_key}
    )
    response.raise_for_status()

    rate = response.json()['rates']['RUB']
    return float(amount) * rate