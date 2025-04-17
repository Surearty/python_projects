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