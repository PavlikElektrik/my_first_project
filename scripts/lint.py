import subprocess
import sys
import argparse

def run(cmd):
    print(f"🔧 Выполняю: {cmd}")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        print(f"❌ Ошибка при выполнении: {cmd}")
        sys.exit(result.returncode)

def lint_directory(path="src"):
    print(f"🔍 Запускаю линтинг для папки: {path}")
    run(f"poetry run black {path}/")
    run(f"poetry run isort {path}/")
    run(f"poetry run flake8 {path}/")
    run(f"poetry run mypy {path}/")
    print("✅ Линтинг успешно завершён!")

def main():
    parser = argparse.ArgumentParser(description="Запуск линтеров для указанной папки")
    parser.add_argument(
        "--path",
        type=str,
        default="src",
        help="Целевая папка для линтинга (по умолчанию: src)"
    )
    args = parser.parse_args()
    lint_directory(args.path)

if __name__ == "__main__":
    main()