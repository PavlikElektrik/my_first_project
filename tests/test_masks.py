import unittest


from src.masks import get_mask_account, get_mask_card_number

class TestMasks(unittest.TestCase):
    def test_get_mask_card_number_valid(self):
        """Тест корректного маскирования номера карты"""
        self.assertEqual(get_mask_card_number("1234567890123456"), "1234 56** **** 3456")
        self.assertEqual(get_mask_card_number("9876123456789012"), "9876 12** **** 9012")

    def test_get_mask_card_number_invalid_length(self):
        """Тест: ошибка при некорректной длине номера карты"""
        with self.assertRaises(ValueError):
            get_mask_card_number("1234")  # Слишком короткий
        with self.assertRaises(ValueError):
            get_mask_card_number("")  # Пустая строка
        with self.assertRaises(ValueError):
            get_mask_card_number("123456789012345")  # Не 16 цифр

    def test_get_mask_card_number_non_digit(self):
        """Тест: ошибка при наличии нецифровых символов в номере карты"""
        with self.assertRaises(ValueError):
            get_mask_card_number("1234abcd5678efgh")

    def test_get_mask_account_valid(self):
        """Тест корректного маскирования номера счёта"""
        self.assertEqual(get_mask_account("12345678901234567890"), "**7890")
        self.assertEqual(get_mask_account("1234"), "**1234")

    def test_get_mask_account_empty(self):
        """Тест: ошибка при пустом номере счёта"""
        with self.assertRaises(ValueError):
            get_mask_account("")

    def test_get_mask_account_non_digit(self):
        """Тест: ошибка при наличии нецифровых символов в номере счёта"""
        with self.assertRaises(ValueError):
            get_mask_account("abcd1234")
        with self.assertRaises(ValueError):
            get_mask_account("1234-абвг")


if __name__ == "__main__":
    unittest.main()
