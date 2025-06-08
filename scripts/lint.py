import subprocess
import sys

def run(cmd):
    print(f" Выполняю: {cmd}")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        print(f" Ошибка при выполнении: {cmd}")
        sys.exit(result.returncode)

def main():
    print("🔍 Запускаю линтинг проекта...")
    run("poetry run black src/")
    run("poetry run isort src/")
    run("poetry run flake8 src/")
    run("poetry run mypy src/")
    print(" Линтинг успешно завершён!")

if __name__ == "__main__":
    main()