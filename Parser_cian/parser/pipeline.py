import csv
import os
from datetime import datetime

class DataPipeline:
    def __init__(self, folder="data"):
        self.folder = folder
        os.makedirs(self.folder, exist_ok=True)

        # Формируем имя файла с текущей датой
        date_str = datetime.now().strftime("%Y-%m-%d")
        self.filename = os.path.join(self.folder, f"output_{date_str}.csv")

    def save_to_csv(self, data):
        if not data:
            print("⚠️ Нет данных для сохранения в CSV.")
            return

        fieldnames = data[0].keys()

        with open(self.filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)

        print(f"💾 CSV сохранён: {self.filename} ({len(data)} записей)")