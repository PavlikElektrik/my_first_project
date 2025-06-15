FROM python:3.12-slim

WORKDIR /app

# 1. Устанавливаем зависимости из requirements.txt (как у вас было)
COPY requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir

# 2. Устанавливаем Poetry (добавляем эту строку)
RUN pip install poetry --no-cache-dir

# 3. Копируем проект (как у вас было)
COPY . .

# 4. Устанавливаем проект через Poetry (ключевое изменение!)
RUN poetry install --no-interaction

# 5. Сохраняем возможность работать в shell
CMD ["bash"]