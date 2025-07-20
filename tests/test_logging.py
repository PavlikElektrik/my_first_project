import unittest
import json
from unittest.mock import patch , mock_open
from src.utils import load_json_data
from src.masks import get_mask_card_number, get_mask_account


class TestLogging(unittest.TestCase):
    @patch("os.path.exists", return_value=True)
    def test_utils_logging(self, mock_exists):
        """Тест логирования успешной загрузки файла"""
        # Подготовка тестовых данных, соответствующих operations.json
        mock_data = json.dumps([
            {
                "id": 441945886,
                "operationAmount": {
                    "amount": "31957.58",
                    "currency": {"code": "RUB"}
                }
            },
            {
                "id": 41428829,
                "operationAmount": {
                    "amount": "8221.37",
                    "currency": {"code": "USD"}
                }
            }
        ])

        # Мокаем открытие файла с нашими тестовыми данными
        with patch("builtins.open", mock_open(read_data=mock_data)) as mock_file:
            with self.assertLogs("utils", level="DEBUG") as logs:
                # Вызываем функцию с путем к файлу
                result = load_json_data("data/operations.json")

                # Проверяем результат
                self.assertEqual(len(result), 2)
                self.assertEqual(result[0]["id"], 441945886)
                self.assertEqual(result[1]["operationAmount"]["currency"]["code"], "USD")

                # Проверяем логи
                self.assertIn("DEBUG:utils:Попытка загрузить файл: data/operations.json", logs.output)
                self.assertIn("INFO:utils:Успешно загружен файл: data/operations.json", logs.output)


class TestMasksLogging(unittest.TestCase):
    def test_card_masking_logging(self):
        with self.assertLogs("masks", level="DEBUG") as logs:
            # Успешное маскирование
            result = get_mask_card_number("1234567890123456")
            self.assertIn("DEBUG:masks:Начало маскирования номера карты: 1234567890123456", logs.output)
            self.assertIn("INFO:masks:Успешно замаскирован номер карты: 1234 56** **** 3456", logs.output)

            # Неудачное маскирование
            with self.assertRaises(ValueError):
                get_mask_card_number("1234")
            self.assertIn("ERROR:masks:Номер карты должен содержать ровно 16 цифр: 1234", logs.output)

    def test_account_masking_logging(self):
        with self.assertLogs("masks", level="DEBUG") as logs:
            # Успешное маскирование
            result = get_mask_account("12345678")
            self.assertIn("DEBUG:masks:Начало маскирования номера счета: 12345678", logs.output)
            self.assertIn("INFO:masks:Успешно замаскирован номер счета: **5678", logs.output)

            # Неудачное маскирование
            with self.assertRaises(ValueError):
                get_mask_account("12ab34")
            self.assertIn("ERROR:masks:Номер счёта должен содержать только цифры: 12ab34", logs.output)
