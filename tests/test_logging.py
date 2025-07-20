import unittest
from unittest.mock import patch
from src.utils import load_json_data
from src.masks import get_mask_card_number, get_mask_account


class TestLogging(unittest.TestCase):
    @patch("builtins.open")
    @patch("os.path.exists", return_value=True)
    def test_utils_logging(self, mock_exists, mock_open):
        with self.assertLogs("utils", level="DEBUG") as logs:
            result = load_json_data("test.json")

            # Проверяем наличие логов
            self.assertIn("DEBUG:utils:Попытка загрузить файл: test.json", logs.output)
            self.assertIn("ERROR:utils:Файл test.json не содержит список", logs.output)


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