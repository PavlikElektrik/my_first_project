import unittest
from unittest.mock import patch
from src.external_api import convert_transaction_to_rub


class TestCurrencyConverter(unittest.TestCase):
    @patch('requests.get')
    def test_usd_conversion(self, mock_get):
        mock_get.return_value.json.return_value = {'rates': {'RUB': 75.0}}
        transaction = {'amount': '100', 'operationCurrency': {'code': 'USD'}}
        result = convert_transaction_to_rub(transaction)
        self.assertEqual(result, 7500.0)

    def test_rub_transaction(self):
        transaction = {'amount': '100', 'operationCurrency': {'code': 'RUB'}}
        result = convert_transaction_to_rub(transaction)
        self.assertEqual(result, 100.0)