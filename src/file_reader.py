import pandas as pd
from typing import List, Dict, Any


def read_csv_file(file_path: str) -> List[Dict[str, Any]]:
    """
    Считывает финансовые операции из CSV-файла.

    Args:
        file_path: Путь к CSV-файлу

    Returns:
        Список словарей с транзакциями
    """
    df = pd.read_csv(file_path, delimiter=';')
    return df.to_dict(orient='records')


def read_excel_file(file_path: str) -> List[Dict[str, Any]]:
    """
    Считывает финансовые операции из XLSX-файла.

    Args:
        file_path: Путь к Excel-файлу

    Returns:
        Список словарей с транзакциями
    """
    df = pd.read_excel(file_path, engine='openpyxl')
    return df.to_dict(orient='records')