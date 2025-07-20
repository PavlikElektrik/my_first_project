import pytest
from unittest.mock import MagicMock, patch
from src.external_api import convert_transaction_to_rub


def test_usd_conversion(mocker):
    """Тест конвертации USD в RUB"""
    # 1. Мокаем os.getenv чтобы вернуть тестовый API ключ
    mocker.patch('os.getenv', return_value='test_api_key')

    # 2. Мокаем requests.get
    mock_get = mocker.patch('requests.get')
    mock_response = MagicMock()
    mock_response.json.return_value = {'success': True, 'result': 7500.0}
    mock_get.return_value = mock_response

    transaction = {
        'operationAmount': {
            'amount': '100',
            'currency': {'code': 'USD'}
        }
    }

    # 3. Вызываем тестируемую функцию
    result = convert_transaction_to_rub(transaction)
    assert result == 7500.0

    # 4. Проверяем параметры вызова
    expected_url = "https://api.apilayer.com/exchangerates_data/convert?to=RUB&from=USD&amount=100"
    mock_get.assert_called_once_with(
        expected_url,
        headers={'apikey': 'test_api_key'}
    )


def test_api_failure(mocker):
    """Тест обработки ошибки API"""
    # Мокаем ответ API
    mock_get = mocker.patch('requests.get')
    mock_response = MagicMock()
    mock_response.json.return_value = {
        'success': False,
        'error': {'info': 'Invalid API key'}
    }
    mock_get.return_value = mock_response

    transaction = {
        'operationAmount': {
            'amount': '100',
            'currency': {'code': 'EUR'}
        }
    }

    with pytest.raises(RuntimeError, match="Invalid API key"):
        convert_transaction_to_rub(transaction)


def test_rub_transaction():
    """Тест рублевой транзакции (без конвертации)"""
    transaction = {
        'operationAmount': {
            'amount': '100',
            'currency': {'code': 'RUB'}
        }
    }
    result = convert_transaction_to_rub(transaction)
    assert result == 100.0


def test_unsupported_currency():
    """Тест неподдерживаемой валюты"""
    transaction = {
        'operationAmount': {
            'amount': '100',
            'currency': {'code': 'JPY'}
        }
    }
    with pytest.raises(ValueError, match="Неподдерживаемая валюта: JPY"):
        convert_transaction_to_rub(transaction)


def test_real_structure(mocker):
    """Тест с реальной структурой из operations.json"""
    # Мокаем API
    mock_get = mocker.patch('requests.get')
    mock_response = MagicMock()
    mock_response.json.return_value = {'success': True, 'result': 600000.0}
    mock_get.return_value = mock_response

    transaction = {
        "id": 41428829,
        "state": "EXECUTED",
        "operationAmount": {
            "amount": "8221.37",
            "currency": {
                "name": "USD",
                "code": "USD"
            }
        }
    }

    result = convert_transaction_to_rub(transaction)
    assert result == 600000.0