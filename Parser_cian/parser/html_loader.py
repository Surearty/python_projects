import requests
from fake_useragent import UserAgent
import time
import random


class HtmlLoader:
    def __init__(self, url):
        self.url = url
        self.ua = UserAgent()
        self.headers = {
            "User-Agent": self.ua.random
        }

    def fetch(self):
        print(f"🌐 Загружаем страницу: {self.url}")
        try:
            response = requests.get(self.url, headers=self.headers, timeout=10)

            if response.status_code == 200:
                print("✅ HTML получен успешно")
                self._anti_ban_sleep()
                return response.text
            else:
                print(f"❌ Ошибка запроса: статус {response.status_code}")
        except Exception as e:
            print(f"💥 Исключение при запросе: {e}")

        return None

    def _anti_ban_sleep(self):
        delay = round(random.uniform(1.5, 3.0), 2)
        print(f"😴 Пауза {delay} сек для антибана...")
        time.sleep(delay)