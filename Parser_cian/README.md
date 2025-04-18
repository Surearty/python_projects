#                       Парсер циан (cian parser)


Для корректной работы парсера мы устанавливаем 4 библиотеки:
📦 1. requests - Просто, быстро и удобно скачивает HTML-страницы с сайтов.
```python
import requests

response = requests.get("https://example.com")
html = response.text
```
🔧 Альтернатива: httpx или aiohttp (если хочешь делать асинхронно)

🍜 2. beautifulsoup4 - Библиотека для парсинга HTML. Очень удобная: можно искать по тегам, классам, структуре.
```Python
from bs4 import BeautifulSoup

soup = BeautifulSoup(html, "lxml")
title = soup.find("h1").text
```

🧠 3. lxml - движок (parser), который BS4 использует “под капотом”, чтобы быстро и надёжно разбирать HTML.

🕵️‍♂️ 4. fake_useragent -Генерирует случайные User-Agent заголовки — как будто ты то с Chrome, то с Safari, то с мобильника.
```python
from fake_useragent import UserAgent

ua = UserAgent()
print(ua.random)
# → Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/...
```

Итого все необходимое окружение мы сохраняем в requirements.txt:
```txt
requests>=2.31.0
beautifulsoup4>=4.12.3
lxml>=4.9.3
fake-useragent>=1.5.1
```
и устанавливаем через терминал:
```bash
pip install -r requirements.txt
```


##                      📦 Архитектура проекта `cian_parser/` 

| Модуль            | Класс / логика                | Ответственность                          |
|------------------|-------------------------------|-------------------------------------------|
| `main.py`         | `Parser.run()`                | Запуск всей цепочки                      |
| `parser.py`       | `Parser`                      | Организует вызов: loader → parser → pipeline |
| `html_loader.py`  | `HtmlLoader`                  | Делает запрос с fake-useragent / прокси  |
| `cian_parser.py`  | `CianParser`                  | Разбирает HTML → list[dict]              |
| `pipeline.py`     | `DataPipeline`                | Сохраняет в CSV (или Excel/DB потом)     |
| `proxy.py`        | `ProxyManager` *(опц.)*       | Вставляет прокси, ротация                |
| `utils.py`        | `clean_text()`, `slugify()`   | Очистка строк, нормализация              |
| `settings.py`     | `HEADERS`, `TIMEOUT`, `CSV_PATH` | Конфиги, не хардкодим в коде          |
| `data/output.csv` | —                             | Готовый результат                         |

## 📦 Класс Parser

Класс Parser — это координирующий компонент проекта. Он организует полный цикл парсинга: от загрузки HTML до сохранения данных в CSV.

### 🔧 Основной функционал:
	•	Получает HTML-код страницы с ЦИАН по заданному URL
	•	Передаёт HTML в CianParser, который извлекает нужные данные (например, заголовок, цену, ссылку)
	•	Передаёт результат в DataPipeline для сохранения в файл (output_ГГГГ-ММ-ДД.csv)
	•	Поддерживает защиту от банов (пауза между запросами, случайный User-Agent)
	•	Работает как единая точка запуска: Parser(url).run()

### 🧩 Использует:
	•	HtmlLoader — отвечает за скачивание страницы
	•	CianParser — отвечает за разбор HTML и извлечение данных
	•	DataPipeline — сохраняет данные в CSV
```python
class Parser:
    def __init__(self, url=BASE_URL):
        self.url = url
        self.loader = HtmlLoader(url)
        self.parser = CianParser()
        self.pipeline = DataPipeline()
```
### 🚀 Пример использования:
```python
from cian_parser.parser import Parser

parser = Parser()
parser.run()
```


## 🌐 Класс HtmlLoader — Загрузка страницы с рендерингом JS

Класс HtmlLoader отвечает за получение полного HTML-кода страницы с ЦИАН, включая все данные, которые подгружаются динамически с помощью JavaScript (такие как цена, адрес, метро и т.д.).

### 🚀 Как работает

Вместо обычного requests, используется браузерный движок Playwright, который:
	•	запускает Chromium в headless-режиме
	•	переходит по указанному URL
	•	дожидается полной загрузки страницы (включая JS)
	•	возвращает финальный HTML, как если бы его увидел обычный пользователь

### 🔧 Основной функционал:
	•	Выполняет HTTP-запрос с помощью requests
	•	Подставляет случайный User-Agent (через fake-useragent)
	•	Поддерживает подключение через прокси (http и https)
	•	Делает случайную паузу (1.5–3.0 сек) после запроса для имитации поведения пользователя
	•	Производит предварительную HEAD-проверку URL на доступность при инициализации
	•	Логирует все события в файл loader.log (успешные и ошибочные запросы)

📦 Пример использования:
```python
from parser_engine.html_loader import HtmlLoader

url = "https://www.cian.ru/sale/flat/315400445/"
loader = HtmlLoader(url)
html = loader.fetch()

# html содержит финальный DOM
```
🛠 Установка зависимостей:
	1.	Убедитесь, что установлен playwright:
```bash
pip install -r requirements.txt
playwright install
```
	2.	Обратите внимание: playwright install необходимо выполнить один раз, чтобы загрузить браузеры.


### 🔍 Что делает метод fetch() внутри HtmlLoader

🔢 Шаг за шагом:
1.	Запуск браузера Chromium в фоне
```python
browser = p.chromium.launch(headless=True)
```
	•	Открывается невидимое (headless) окно браузера
	•	Это даёт возможность подгрузить JS, не открывая реальное окно

2.	Создание изолированного контекста
```python
context = browser.new_context()
```
    •	Создаётся новая “сессия браузера” — со своими куками, заголовками и окружением
	•	Можно подменять UA, выставлять геолокацию и т.д. (если нужно)

3.	Открытие новой вкладки
```python
page = context.new_page()
```

4.	Переход на указанный URL
```python
page.goto(self.url)
```
	•	Playwright загружает страницу, включая все JS-ресурсы
	•	Он по умолчанию ждёт окончания DOMContentLoaded, но мы добавим паузу для гарантии

5.	Ожидание полной подгрузки JS-контента
```python
time.sleep(random.uniform(2.5, 4.0))
```
    •	Эта задержка даёт браузеру время “дотянуть” динамические данные (цена, адрес, метро)
	•	Потом можно будет заменить на более умное ожидание (например, page.wait_for_selector)

6.	Извлечение финального DOM
```python
html = page.content()
```
	•	Возвращается HTML-код в виде строки — он уже включает всё, что “отрисовал” JS
	•	Это полноценная копия кода, как его увидел бы пользователь

7.	Закрытие браузера
```python
browser.close()
```

### 📌 Итого

fetch() делает то, что не может requests:
он эмулирует живой браузер, прогружает весь контент, и возвращает реально “живой” HTML, пригодный для парсинга.


