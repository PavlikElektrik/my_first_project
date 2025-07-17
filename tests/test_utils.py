import unittest
from unittest.mock import patch
from src.utils import load_json_data
import json

class TestJsonLoader(unittest.TestCase):
    @patch('builtins.open')
    def test_file_not_found(self, mock_open):
        mock_open.side_effect = FileNotFoundError
        result = load_json_data('missing.json')
        self.assertEqual(result, [])

    @patch('json.load')
    @patch('builtins.open')
    def test_invalid_json(self, mock_open, mock_load):
        mock_load.side_effect = json.JSONDecodeError("Error", "doc", 0)
        result = load_json_data('invalid.json')
        self.assertEqual(result, [])