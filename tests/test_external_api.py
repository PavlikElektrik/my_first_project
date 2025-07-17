import os
import unittest
from unittest.mock import patch, MagicMock
from src.external_api import convert_transaction_to_rub

class TestCurrencyConverter(unittest.TestCase):
    def test_rub_transaction(self):
        """Тест для транзакции в рублях (конвертация не требуется)"""
        transaction = {'amount': '500', 'operationCurrency': {'code': 'RUB'}}
        result = convert_transaction_to_rub(transaction)
        self.assertEqual(result, 500.0)

    def test_unsupported_currency(self):
        """Тест для неподдерживаемой валюты"""
        transaction = {'amount': '100', 'operationCurrency': {'code': 'JPY'}}
        with self.assertRaises(ValueError):
            convert_transaction_to_rub(transaction)

    @patch.dict(os.environ, {"API_KEY_EXCHANGERATES": "YOUR_MOCKED_API_KEY"})
    @patch('requests.get')
    def test_usd_conversion(self, mock_get):
        """Тест конвертации USD в RUB"""
        # Мокаем ответ API
        mock_response = MagicMock()
        mock_response.json.return_value = {'success': True, 'result': 7500.0}
        mock_get.return_value = mock_response

        transaction = {'amount': '100', 'operationCurrency': {'code': 'USD'}}
        result = convert_transaction_to_rub(transaction)
        self.assertEqual(result, 7500.0)

        # Проверяем параметры запроса
        mock_get.assert_called_with(
            "https://api.apilayer.com/exchangerates_data/convert?to=RUB&from=USD&amount=100",
            headers={'apikey': 'YOUR_MOCKED_API_KEY'}
        )

    @patch.dict(os.environ, {"API_KEY_EXCHANGERATES": "YOUR_MOCKED_API_KEY"})
    @patch('requests.get')
    def test_api_failure(self, mock_get):
        """Тест обработки ошибки API"""
        # Мокаем ошибку API
        mock_response = MagicMock()
        mock_response.json.return_value = {'success': False, 'error': {'info': 'Invalid API Key'}}
        mock_response.raise_for_status.side_effect = None
        mock_get.return_value = mock_response

        transaction = {'amount': '100', 'operationCurrency': {'code': 'USD'}}
        with self.assertRaises(RuntimeError):
            convert_transaction_to_rub(transaction)