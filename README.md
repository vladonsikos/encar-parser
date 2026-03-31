# Encar Parser & Landing Page

Парсер автомобилей с [encar.com](https://www.encar.com) + адаптивный лендинг.

## Структура

```
encar_parser.py   — парсер (корейские + импортные авто, retry, сохранение в cars.json)
scheduler.py      — запуск парсера сразу + каждые 24 часа
server.py         — Flask сервер (лендинг + /api/cars)
static/
  index.html      — лендинг
  style.css       — стили (тёмная тема, адаптив)
  app.js          — загрузка данных, карточки, поиск
```

## Установка

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Запуск

```bash
# 1. Собрать данные
python3 encar_parser.py

# 2. Запустить сервер
python3 server.py
# → http://localhost:5000

# Или запустить планировщик (парсит сразу + каждые 24ч)
python3 scheduler.py
```

## API

- `GET /` — лендинг
- `GET /api/cars` — JSON с данными автомобилей
