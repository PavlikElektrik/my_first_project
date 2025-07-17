import unittest
from unittest.mock import patch, mock_open
import json
from src.utils import load_json_data


class TestJsonLoader(unittest.TestCase):

    @patch("os.path.exists", return_value=True)
    @patch("builtins.open", new_callable=mock_open, read_data='[{"id": 1}]')
    def test_success_load(self, mock_file, mock_exists):
        """Тест успешной загрузки валидного JSON"""
        result = load_json_data("valid.json")
        self.assertEqual(result, [{"id": 1}])

    @patch("os.path.exists", return_value=True)
    @patch("builtins.open", new_callable=mock_open, read_data='{"id": 1}')
    def test_not_list_data(self, mock_file, mock_exists):
        """Тест когда JSON не является списком"""
        result = load_json_data("not_list.json")
        self.assertEqual(result, [])

    @patch("os.path.exists", return_value=True)
    @patch("builtins.open", side_effect=OSError)
    def test_os_error(self, mock_file, mock_exists):
        """Тест обработки OSError"""
        result = load_json_data("error.json")
        self.assertEqual(result, [])

    @patch("os.path.exists", return_value=True)
    @patch("builtins.open", new_callable=mock_open, read_data='')
    def test_empty_file(self, mock_file, mock_exists):
        """Тест пустого файла"""
        result = load_json_data("empty.json")
        self.assertEqual(result, [])
