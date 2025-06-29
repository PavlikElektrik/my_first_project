# Банковские операции — анализ данных

Цель проекта — реализовать набор функций для обработки данных о банковских операциях.  
Функционал включает:
- Фильтрацию операций по статусу
- Сортировку операций по дате
- Маскировку номеров карт и счетов
- Преобразование формата даты

---

## Установка

Проект использует [Poetry](https://python-poetry.org/)  для управления зависимостями.

### Требования:
- Python 3.8+
- Poetry установлен

### Шаги установки:

1. Клонируйте репозиторий:
```
git clone https://github.com/PavlikElektrik/my_first_project
```
2. Установите зависимости:
```
poetry install
```

## Использование

В проекте реализованы следующие функции:

**1. filter_by_state(operations, state='EXECUTED')**
Фильтрует список операций по значению ключа 'state'.
```
from utils import filter_by_state

filtered = filter_by_state(operations)
```
**2. sort_by_date(operations, reverse=True)**
Сортирует список операций по дате (по умолчанию — по убыванию).
```
from utils import sort_by_date

sorted_operations = sort_by_date(operations)
```
**3. mask_account_card(card_or_account_info: str) -> str**
Маскирует номер карты или счёта по правилам:
Карта: XXXX XX** **** XXXX
Счёт: **XXXX
```
from masks import mask_account_card

masked = mask_account_card("Visa Platinum 7000792289606365")
```
**4. get_date(date_str: str) -> str**
Преобразует дату из формата ISO в формат ДД.ММ.ГГГГ.
```
from utils import get_date

formatted_date = get_date("2024-03-11T02:26:18.671407")
```
**Пример входных данных**
```
operations = [
    {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
    {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
    {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
    {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}
]
```

## Лицензия

Проект распространяется под [лицензией MIT](LICENSE).  
Это означает, что вы можете свободно использовать, изменять и распространять код, даже в коммерческих целях, при условии сохранения уведомления об авторстве и лицензии.

Полный текст лицензии доступен в файле [`LICENSE`](LICENSE).
