import unittest
from unittest.mock import patch, mock_open
from src.file_reader import read_csv_file, read_excel_file
import pandas as pd


class TestFileReader(unittest.TestCase):
    @patch('pandas.read_csv')
    def test_read_csv_file(self, mock_read_csv):
        """Тест чтения CSV-файла"""
        test_data = pd.DataFrame({
            'date': ['2023-01-01'],
            'amount': [100],
            'description': ['Test']
        })
        mock_read_csv.return_value = test_data

        result = read_csv_file('dummy.csv')
        self.assertEqual(result, [
            {'date': '2023-01-01', 'amount': 100, 'description': 'Test'}
        ])

    @patch('pandas.read_excel')
    def test_read_excel_file(self, mock_read_excel):
        """Тест чтения XLSX-файла"""
        test_data = pd.DataFrame({
            'date': ['2023-01-02'],
            'amount': [200],
            'category': ['Finance']
        })
        mock_read_excel.return_value = test_data

        result = read_excel_file('dummy.xlsx')
        self.assertEqual(result, [
            {'date': '2023-01-02', 'amount': 200, 'category': 'Finance'}
        ])


if __name__ == '__main__':
    unittest.main()