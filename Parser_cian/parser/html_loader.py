from playwright.sync_api import sync_playwright
import time
import random
import logging

class HtmlLoader:
    def __init__(self, url):
        self.url = url
        logging.basicConfig(
            filename="loader.log",
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(message)s"
        )

    def fetch(self):
        print(f"🌐 Загружаем страницу через Playwright: {self.url}")
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                context = browser.new_context()
                page = context.new_page()
                page.goto(self.url)
                time.sleep(random.uniform(2.5, 4.0))  # ждать, пока подтянется JS
                html = page.content()
                print("✅ HTML с рендерингом получен")
                browser.close()
                return html
        except Exception as e:
            print(f"💥 Ошибка Playwright: {e}")
            logging.error(f"Exception in Playwright: {e}")
            return None