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


## 🌐 Класс HtmlLoader

Класс HtmlLoader отвечает за безопасную и гибкую загрузку HTML-кода веб-страницы по заданному URL.
Он включает в себя поддержку антибана, работу с прокси, логирование и первичную проверку доступности ресурса.

### 🔧 Основной функционал:
	•	Выполняет HTTP-запрос с помощью requests
	•	Подставляет случайный User-Agent (через fake-useragent)
	•	Поддерживает подключение через прокси (http и https)
	•	Делает случайную паузу (1.5–3.0 сек) после запроса для имитации поведения пользователя
	•	Производит предварительную HEAD-проверку URL на доступность при инициализации
	•	Логирует все события в файл loader.log (успешные и ошибочные запросы)

📄 Пример логов (loader.log):
```
2025-04-17 12:42:01 [INFO] Success: https://www.cian.ru/...
2025-04-17 12:43:05 [WARNING] Bad status 403 for https://www.cian.ru/...
2025-04-17 12:44:21 [ERROR] Exception: HTTPSConnectionPool(...)
```

🔐 Прокси и URL можно задать через .env:
```env
CIAN_URL=https://www.cian.ru/...
PROXY_HTTP=http://123.45.67.89:8080
PROXY_HTTPS=http://123.45.67.89:8080
```
И использовать в settings.py:
```python
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("CIAN_URL")
PROXIES = {
    "http": os.getenv("PROXY_HTTP"),
    "https": os.getenv("PROXY_HTTPS")
}
```

## 🧩 Использует:
	•	fake-useragent — генерация случайных User-Agent заголовков
	•	requests — выполнение HTTP-запросов
	•	logging — логирование действий в файл loader.log
	•	dotenv — загрузка конфигурации из .env
	•	random + time.sleep — реализация паузы для обхода антибот-систем

class html_loader:
```python
class HtmlLoader:
    def __init__(self, url, proxies=None):
        self.url = url
        self.ua = UserAgent()
        self.headers = {
            "User-Agent": self.ua.random
        }
        self.proxies = proxies

        # Настраиваем логгер
        logging.basicConfig(
            filename="loader.log",
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(message)s"
        )

        if not self._check_url():
            print("⚠️ Предупреждение: URL может быть недоступен.")
            logging.warning(f"URL may be unreachable: {self.url}")

    def fetch(self):
        print(f"🌐 Загружаем страницу: {self.url}")
        try:
            response = requests.get(
                self.url,
                headers=self.headers,
                proxies=self.proxies,
                timeout=10
            )

            if response.status_code == 200:
                print("✅ HTML получен успешно")
                logging.info(f"Success: {self.url}")
                self._anti_ban_sleep()
                return response.text
            else:
                print(f"❌ Ошибка запроса: статус {response.status_code}")
                logging.warning(f"Bad status {response.status_code} for {self.url}")
        except Exception as e:
            print(f"💥 Исключение при запросе: {e}")
            logging.error(f"Exception: {e}")

        return None

    def _anti_ban_sleep(self):
        delay = round(random.uniform(1.5, 3.0), 2)
        print(f"😴 Пауза {delay} сек для антибана...")
        time.sleep(delay)

    def _check_url(self):
        """Простая HEAD-проверка доступности URL"""
        try:
            response = requests.head(self.url, timeout=5)
            return response.status_code < 400
        except Exception:
            return False
```
### ✅ Что внутри def fetch(self) `response` (объект `requests.get(...)`)

| Атрибут / метод                        | Что даёт                                        | Пример                                           |
|---------------------------------------|--------------------------------------------------|--------------------------------------------------|
| `response.status_code`                | Код ответа сервера                               | `200`, `403`, `404`, `500`                       |
| `response.text`                       | HTML содержимое страницы как строка              | `"<html>...</html>"`                             |
| `response.content`                    | HTML как `bytes` (для изображений и файлов)      | `b"<html>...</html>"`                            |
| `response.headers`                    | Заголовки ответа                                 | `{'Content-Type': 'text/html; charset=utf-8'}`   |
| `response.url`                        | Итоговый URL (с учётом редиректов)              | `"https://www.cian.ru/cat.php?...`"             |
| `response.ok`                         | `True`, если статус от 200 до 399                | `True` / `False`                                 |
| `response.encoding`                   | Кодировка текста                                 | `"utf-8"`                                        |
| `response.elapsed.total_seconds()`   | Время ответа от сервера                          | `0.42` (секунд)                                  |

