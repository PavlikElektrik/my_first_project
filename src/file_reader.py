from typing import Any, Dict, List

import pandas as pd
from pandas import DataFrame


def read_csv_file(file_path: str) -> List[Dict[str, Any]]:
    """
    Считывает финансовые операции из CSV-файла.

    Args:
        file_path: Путь к CSV-файлу

    Returns:
        Список словарей с транзакциями (ключи - строки)
    """
    df: DataFrame = pd.read_csv(file_path, delimiter=";")
    # Преобразуем DataFrame в список словарей с явным указанием типа ключей
    return _convert_records(df.to_dict(orient="records"))


def read_excel_file(file_path: str) -> List[Dict[str, Any]]:
    """
    Считывает финансовые операции из XLSX-файла.

    Args:
        file_path: Путь к Excel-файлу

    Returns:
        Список словарей с транзакциями (ключи - строки)
    """
    df: DataFrame = pd.read_excel(file_path, engine="openpyxl")
    # Преобразуем DataFrame в список словарей с явным указанием типа ключей
    return _convert_records(df.to_dict(orient="records"))


def _convert_records(records: List[Dict[Any, Any]]) -> List[Dict[str, Any]]:
    """Преобразует записи с любыми ключами в записи со строковыми ключами"""
    return [{str(key): value for key, value in record.items()} for record in records]
