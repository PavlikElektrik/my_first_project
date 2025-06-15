# scripts/run_tests.py
import pytest
import sys
from pathlib import Path

def main():
    sys.exit(pytest.main(["tests/tests.py", "-v"]))


def coverage():
    """Генерация отчета о покрытии"""
    # Создаем папку для отчетов если её нет
    report_dir = Path("htmlcov")
    report_dir.mkdir(exist_ok=True)

    # Запускаем тесты с покрытием
    pytest.main([
        "tests/tests.py",
        "--cov=src",
        "--cov-report=html:htmlcov",
        "--cov-report=term-missing"
    ])

    print(f"\nОтчет покрытия сохранен в: {report_dir.absolute()}/index.html")


if __name__ == "__main__":
    main()
    coverage()
