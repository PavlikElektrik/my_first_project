# src/main.py
from typing import Any, Dict, List

from src.decorators import log

# Чтение файлов
from src.file_reader import read_csv_file, read_excel_file
from src.generators import filter_by_currency
from src.logger import setup_logger

# Обработка/фильтрация
from src.processing import filter_by_state, format_operation, sort_by_date

# Новые функции из задания
from src.regex_utils import process_bank_operations, process_bank_search
from src.utils import load_json_data

VALID_STATUSES = {"EXECUTED", "CANCELED", "PENDING"}
"""
main.py — точка входа в приложение обработки банковских транзакций.

Функции:
- Загрузка данных из JSON, CSV или Excel.
- Фильтрация по статусу.
- Сортировка по дате.
- Фильтрация по валюте.
- Поиск по описанию операций.
- Подсчёт количества операций по ключевым категориям.
- Форматированный вывод в лог.

Запуск:
    python src/main.py
"""


@log(filename="logs/main.log")
def main() -> None:
    """
    Основная точка входа в программу для обработки банковских операций.

    Последовательность действий:
    1. Запрашивает источник данных (JSON, CSV, Excel).
    2. Загружает и валидирует операции.
    3. Фильтрует операции по статусу (EXECUTED, CANCELED, PENDING).
    4. При необходимости сортирует операции по дате.
    5. Фильтрует по валюте (только рублевые).
    6. Позволяет искать по описанию (через регулярные выражения).
    7. Считает количество операций по заданным категориям.
    8. Выводит отформатированный список операций в лог.

    Логи записываются в logs/main.log.
    """
    logger = setup_logger("main")
    print("Добро пожаловать в приложение для обработки банковских транзакций.")
    print("Выберите формат файла, который вы хотите обработать:")
    print("1 — JSON")
    print("2 — CSV")
    print("3 — Excel (XLSX)")
    logger.info("Запуск программы работы с банковскими транзакциями")

    # 1) Источник данных

    handlers = {
        "1": load_json_data,
        "2": read_csv_file,
        "3": read_excel_file,
    }
    while True:
        choice = input("Ваш выбор (1/2/3): ").strip()
        if choice in handlers:
            break
        print("Неверный выбор. Пожалуйста, введите 1, 2 или 3.")

    path = input("Введите путь к файлу: ").strip()
    logger.info("Выбран формат %s, путь: %s", choice, path)

    data: List[Dict[str, Any]] = handlers[choice](path)
    logger.info("Загружено %d операций", len(data))

    try:
        operations: List[Dict[str, Any]] = handlers[choice](path)
    except Exception as e:
        logger.exception("Ошибка при чтении файла: %s", e)
        print("Ошибка при чтении файла. Проверьте путь и формат.")
        return

    logger.info("Загружено %d операций", len(operations))
    data = operations

    # 2) Фильтрация по статусу
    while True:
        status = input(f"Введите статус для фильтрации ({', '.join(VALID_STATUSES)}): ").strip().upper()
        if status in VALID_STATUSES:
            data = filter_by_state(data, status)
            logger.info("Отфильтровано по статусу %s: %d операций", status, len(data))
            break
        print("Неверный статус. Попробуйте ещё раз.")
        logger.warning("Неверный статус: %s", status)

    # 3) Сортировка по дате
    if input("Отсортировать по дате? Да/Нет: ").strip().lower() == "да":
        order = input("По возрастанию или по убыванию? ").strip().lower()
        reverse = not order.startswith("в")
        data = sort_by_date(data, reverse=reverse)
        logger.info("Отсортировано по дате (%s)", "убыв." if reverse else "возр.")

    # 4) Фильтр по валюте
    if input("Только рублевые? Да/Нет: ").strip().lower() == "да":
        data = list(filter_by_currency(data, "руб."))
        logger.info("Оставлены рублевые: %d операций", len(data))

    # 5) Поиск по описанию (реgex)
    if input("Поиск по слову в описании? Да/Нет: ").strip().lower() == "да":
        term = input("Введите слово: ").strip()
        data = process_bank_search(data, term)
        logger.info("После поиска '%s': %d операций", term, len(data))

    # 6) Подсчёт по категориям (пример)
    categories = ["Перевод", "Открытие", "Оплата"]
    stats = process_bank_operations(data, categories)
    logger.info("Статистика по категориям: %s", stats)

    # 7) Вывод результатов
    if not data:
        logger.info("Ни одной операции не нашлось.")
        print("Ни одной операции не найдено по заданным фильтрам.")
        return

    logger.info("Итоговый список операций (%d):", len(data))
    for op in data:
        logger.info("\n" + format_operation(op))


if __name__ == "__main__":
    main()
