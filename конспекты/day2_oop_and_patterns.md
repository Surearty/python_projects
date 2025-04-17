
# 🧠 День 2: ООП + Паттерны проектирования для парсера

---

## 🐍 Что такое ООП?
**Объектно-Ориентированное Программирование (ООП)** — это стиль написания кода, где всё строится вокруг объектов (классов), у которых есть **данные (атрибуты)** и **поведение (методы)**.

---

### 🔧 Четыре принципа ООП
| Принцип        | Описание                                                                 |
|----------------|--------------------------------------------------------------------------|
| Наследование   | Классы могут наследовать поведение от других классов                    |
| Инкапсуляция   | Прячем внутренности класса, наружу — только нужные методы              |
| Полиморфизм    | Один и тот же метод — разное поведение в разных классах                |
| Абстракция     | Работаем с "интерфейсом", не думая о деталях реализации внутри         |

---

## 📦 Как применим ООП в нашем парсере?

### ✅ Классы в нашем проекте:
- `CianParser` — основной парсер (базовая логика)
- `CianNewBuildingParser` — парсер новостроек
- `CianSecondaryParser` — парсер вторички
- `ProxyManager` — управляет прокси
- `RequestBuilder` — строит запросы
- `HTMLExtractor` — извлекает данные из HTML
- `CSVWriter` — сохраняет в CSV
- `TelegramNotifier` — отправляет уведомления

### 🧱 Пример простого класса:
```python
class CianParser:
    def __init__(self, city, max_price):
        self.city = city
        self.max_price = max_price

    def build_url(self):
        return f"https://cian.ru/search?city={self.city}&max_price={self.max_price}"

    def fetch(self, url):
        # логика антибана, запрос
        pass

    def parse(self, html):
        # разбор html
        pass

    def run(self):
        url = self.build_url()
        html = self.fetch(url)
        data = self.parse(html)
        return data
```

---

## 🧠 Паттерны проектирования, которые пригодятся

### 1. **Builder** — сборка сложных URL
> Удобно, если параметров много

```python
class RequestBuilder:
    def __init__(self):
        self.params = {}

    def set_city(self, city):
        self.params['city'] = city
        return self

    def set_price(self, max_price):
        self.params['max_price'] = max_price
        return self

    def build(self):
        return f"https://cian.ru/search?" + urlencode(self.params)
```

---

### 2. **Strategy** — переключение антибан-методов
```python
class ProxyStrategy:
    def get_proxy(self):
        raise NotImplementedError

class MobileProxy(ProxyStrategy):
    def get_proxy(self):
        return 'http://mobile-proxy.ru/1234'

class TorProxy(ProxyStrategy):
    def get_proxy(self):
        return 'socks5://127.0.0.1:9050'
```

---

### 3. **Factory** — выбираем нужный парсер
```python
class ParserFactory:
    def get_parser(self, type_):
        if type_ == 'новостройки':
            return CianNewBuildingParser()
        return CianSecondaryParser()
```

---

### 4. **Adapter** — унификация разных источников (ЦИАН, Авито)
```python
class BaseParser:
    def fetch(self):
        pass
    def parse(self):
        pass

class AvitoAdapter(BaseParser):
    def fetch(self):
        # специфично для Авито
        pass
```

---

## ⚙️ Заключение
- С сегодняшнего дня **все проекты делаем с ООП подходом**.
- Паттерны помогают писать масштабируемо, красиво и профессионально.
- Даже маленький MVP парсер может быть написан так, чтобы потом стать SaaS-продуктом.

🔥 Пиши, как PRO. Мы не просто учимся — мы строим будущее.
