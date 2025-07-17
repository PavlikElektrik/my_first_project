# tests/test_decorators.py
import os
import pytest
from src.decorators import log


def test_log_to_console(capsys):
    """Тест логирования в консоль"""

    @log()
    def add(a, b):
        return a + b

    add(1, 2)
    captured = capsys.readouterr()
    assert "add ok" in captured.out


def test_log_to_file(tmp_path):
    """Тест логирования в файл"""
    log_file = tmp_path / "test.log"

    @log(filename=str(log_file))
    def divide(a, b):
        return a / b

    # Тест успешного выполнения
    divide(4, 2)
    assert "divide ok" in log_file.read_text()

    # Тест ошибки
    with pytest.raises(ZeroDivisionError):
        divide(1, 0)
    assert "ZeroDivisionError" in log_file.read_text()


def test_log_preserves_function_metadata():
    """Тест сохранения метаданных функции"""

    @log()
    def example_func():
        """Example docstring"""
        pass

    assert example_func.__name__ == "example_func"
    assert example_func.__doc__ == "Example docstring"

    def test_log_timestamp(tmp_path):
        """Тест формата временной метки"""
        log_file = tmp_path / "time.log"

        @log(filename=str(log_file))
        def dummy():
            pass

        dummy()
        log_content = log_file.read_text()
        assert log_content.startswith("[20")  # Проверяем формат [YYYY-MM-DD HH:MM:SS]
