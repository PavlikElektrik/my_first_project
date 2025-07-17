import os
import requests
from dotenv import load_dotenv
from typing import Dict, Union

load_dotenv()


def convert_transaction_to_rub(transaction: Dict[str, Union[str, Dict]]) -> float:
    """
    Конвертирует сумму транзакции в рубли, используя внешний API.
    Использует endpoint 'convert' вместо 'latest' для прямой конвертации.

    Аргументы:
        transaction: Словарь с данными о транзакции

    Возвращает:
        Сумму в рублях (float)

    Вызывает:
        ValueError: Для неподдерживаемых валют
        RuntimeError: При ошибках API или отсутствии ключа
    """
    # Извлекаем данные из транзакции
    amount = transaction['amount']
    currency = transaction['operationCurrency']['code']

    # Для рублевых транзакций конвертация не нужна
    if currency == 'RUB':
        return float(amount)

    # Проверяем поддерживаемые валюты
    if currency not in ('USD', 'EUR'):
        raise ValueError(f"Неподдерживаемая валюта: {currency}")

    # Получаем API ключ из переменных окружения
    api_key = os.getenv('API_KEY_EXCHANGERATES')
    if not api_key:
        raise RuntimeError("API ключ для конвертации валют не найден")

    try:
        # Используем endpoint 'convert' для прямой конвертации
        response = requests.get(
            f"https://api.apilayer.com/exchangerates_data/convert?"
            f"to=RUB&from={currency}&amount={amount}",
            headers={'apikey': api_key}
        )

        # Проверяем статус ответа
        response.raise_for_status()

        # Извлекаем результат конвертации
        result = response.json()
        if not result.get('success', False):
            raise RuntimeError(f"API error: {result.get('error', {}).get('info', 'Unknown error')}")

        return float(result['result'])

    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Ошибка при обращении к API: {str(e)}") from e