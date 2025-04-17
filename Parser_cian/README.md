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

#                                  Структура программы

## 📦 Архитектура проекта `cian_parser/` 

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