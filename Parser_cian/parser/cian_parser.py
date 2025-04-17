from bs4 import BeautifulSoup

class CianParser:
    def __init__(self):
        pass

    def parse(self, html):
        soup = BeautifulSoup(html, "lxml")
        flats = []

        # Находим все блоки с объявлениями
        listings = soup.find_all("article", class_="_93444fe79c--container--Povoi")

        print(f"🔍 Найдено объявлений: {len(listings)}")

        for item in listings:
            # Название (заголовок)
            title_el = item.find("span", class_="_93444fe79c--title--vX4bF")
            title = title_el.text.strip() if title_el else "N/A"

            # Цена
            price_el = item.find("span", class_="_93444fe79c--price--uZCZb")
            price = price_el.text.strip() if price_el else "N/A"

            # Ссылка
            link_el = item.find("a", href=True)
            link = f"https://www.cian.ru{link_el['href']}" if link_el else "N/A"

            flats.append({
                "title": title,
                "price": price,
                "link": link
            })

        return flats