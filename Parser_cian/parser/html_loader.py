import requests
from fake_useragent import UserAgent
import time
import random
import logging

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