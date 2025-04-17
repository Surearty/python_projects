import requests
from bs4 import BeautifulSoup
import csv
import time
import random
from fake_useragent import UserAgent

class Parser:
    def __init__(self, url):
        self.url = url
        self.ua = UserAgent()
        self.headers = {
            "User-Agent": self.ua.random
        }

    def fetch_html(self):
        print(f"🌐 Загружаем: {self.url}")
        try:
            response = requests.get(self.url, headers=self.headers, timeout=10)
            if response.status_code == 200:
                print("✅ HTML получен успешно")
                return response.text
            else:
                print(f"❌ Ошибка: статус {response.status_code}")
        except Exception as e:
            print(f"❌ Ошибка при запросе: {e}")
        return None

    def parse(self, html):
        soup = BeautifulSoup(html, "lxml")
        flats = []

        listings = soup.find_all("article", class_="_93444fe79c--container--Povoi")  # может измениться!
        print(f"🔍 Найдено объявлений: {len(listings)}")

        for item in listings:
            title = item.find("span", class_="_93444fe79c--title--vX4bF")
            price = item.find("span", class_="_93444fe79c--price--uZCZb")

            flats.append({
                "title": title.text.strip() if title else "N/A",
                "price": price.text.strip() if price else "N/A"
            })

        return flats

    def save_to_csv(self, data):
        with open("cian_output.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["title", "price"])
            writer.writeheader()
            for row in data:
                writer.writerow(row)
        print(f"💾 Сохранено: {len(data)} объектов → cian_output.csv")

    def run(self):
        html = self.fetch_html()
        if html:
            time.sleep(random.uniform(1.5, 3.0))  # ⏱ антибан
            data = self.parse(html)
            self.save_to_csv(data)