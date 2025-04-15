import pandas as pd
import os

# Загружаем CSV
df = pd.read_csv("циан.csv", sep=";")  # Укажи sep, если нужно
# Удаляем не нужные колонки
df = df.drop(columns=["Описание", 'Лифт'])
df.to_csv("cian_clear.csv", index=False, sep=";")
# Взяли новый очищенный файл
df = pd.read_csv("cian_clear.csv", sep=";")

df.columns = df.columns.str.strip()        # убираем пробелы по краям
df.columns = df.columns.str.replace('\n', '')  # убираем переносы строк
# Распечатали информацию о данных
# print(df.info()) 
# Распечатали первые 5 строк
# print(df.head())

# print(f'✅ Количество обьявлений в файле = {len(df)}')  
# Добавляем новый столбец с ценой int
df["Цена_число"] = df["Цена"].apply(lambda x: int(x.split()[0]))
# Теперь можно посчитать среднюю цену
average_price = df["Цена_число"].mean()
print(f"✅ Средняя цена: {average_price:,.0f} ₽")
median_price = df["Цена_число"].median()
print(f"✅ Медианная цена: {median_price:,.0f} ₽")
min_price = df["Цена_число"].min()

# Добавляем новый столбец с площадью float
df["Площадь"] = df["Площадь, м2"].apply(lambda x: float(x.split('/')[0]))
# 1. Находим строку с минимальной ценой
min_row = df[df["Цена_число"] == df["Цена_число"].min()].iloc[0]

# 2. Достаём из неё нужные поля
min_price = min_row["Цена_число"]
area = min_row["Площадь"]
zhk = min_row["Название ЖК"]
metro = min_row["Метро"]

# 3. Выводим всё в красивом формате
print(f"✅ Минимальная цена: {min_price:,.0f} ₽ за {area} м² в ЖК «{zhk}», метро {metro}")

# 1. Находим строку с максимальной ценой
max_row = df[df["Цена_число"] == df["Цена_число"].max()].iloc[0]

# 2. Достаём из неё нужные поля
max_price = max_row["Цена_число"]
area = max_row["Площадь"]
zhk = max_row["Название ЖК"]
metro = max_row["Метро"]

# 3. Выводим всё в красивом формате
print(f"✅ Максимальная цена: {max_price:,.0f} ₽ за {area} м² в ЖК «{zhk}», метро {metro}")

# print(f'✅ Количество обьявлений в файле = {len(df)}') 