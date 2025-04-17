from .html_loader import HtmlLoader
from .cian_parser import CianParser
from .pipeline import DataPipeline
from .settings import BASE_URL


class Parser:
    def __init__(self, url=BASE_URL):
        self.url = url
        self.loader = HtmlLoader(url)
        self.parser = CianParser()
        self.pipeline = DataPipeline()

    def run(self):
        print("🚀 Парсер запущен")

        html = self.loader.fetch() # html — строка str, содержащая весь HTML-код страницы.   
        if not html:
            print("❌ Не удалось получить HTML")
            return

        data = self.parser.parse(html)  # метод parse(html) возвращает list[dict] — то есть список словарей
        if not data:
            print("⚠️ Нет данных для сохранения")
            return

        self.pipeline.save_to_csv(data) # сохраняем в .csv
        print("✅ Парсинг завершён")