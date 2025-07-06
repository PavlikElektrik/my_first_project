# src/decorators.py
from datetime import datetime
from typing import Callable, Any, Optional, TextIO
import functools


def log(filename: Optional[str] = None) -> Callable:
    """
    Декоратор для логирования работы функций.

    Args:
        filename: Имя файла для записи логов. Если None - вывод в консоль.

    Returns:
        Декорированную функцию с логированием.
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            start_time = datetime.now()
            func_name = func.__name__
            log_message = ""

            try:
                result = func(*args, **kwargs)
                log_message = f"{func_name} ok\n"
                return result
            except Exception as e:
                log_message = f"{func_name} error: {type(e).__name__}. Inputs: {args}, {kwargs}\n"
                raise
            finally:
                timestamp = start_time.strftime("%Y-%m-%d %H:%M:%S")
                full_log = f"[{timestamp}] {log_message}"

                if filename:
                    with open(filename, "a", encoding="utf-8") as f:
                        f.write(full_log)
                else:
                    print(full_log, end="")

        return wrapper

    return decorator