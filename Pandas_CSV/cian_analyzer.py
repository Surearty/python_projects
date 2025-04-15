import pandas as pd
import os
def print_df(header, df):
    print()
    print()
    print(header)
    for i, row in df.iterrows():
        print(f"🏠 {row['Адрес']} | {row["Площадь"]} м² | "
        f"{row['Цена_число']:,.0f} ₽ | "
        f"{row['Цена_за_м2']:,.0f} ₽/м² | ЖК: {row['Название ЖК']} | Метро: {row['Метро']}")

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


#                  Рассчитываем количество обьявлений в файле

# print(f'✅ Количество обьявлений в файле = {len(df)}')  


#                   Рассчитываем среднюю и медианную цену

# Добавляем новый столбец с ценой int
df["Цена_число"] = df["Цена"].apply(lambda x: int(x.split()[0]))
# Теперь можно посчитать среднюю цену
average_price = df["Цена_число"].mean()
print(f"✅ Средняя цена: {average_price:,.0f} ₽")
median_price = df["Цена_число"].median()
print(f"✅ Медианная цена: {median_price:,.0f} ₽")


#               Рассчитываем минимальную и максимальную цену

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


#               Рассчитываем среднюю цену квадратного метра
# 1. Считаем цену за м²
df["Цена_за_м2"] = df["Цена_число"] / df["Площадь"]
# 2. Считаем среднюю цену за м²
avg_price_per_m2 = df["Цена_за_м2"].mean()
# 3. Красиво выводим
print(f"📊 Средняя цена за квадратный метр: {avg_price_per_m2:,.0f} ₽/м²")
print()

#                      Выводим ТОП-5 самых дешевых
# Сортируем по возрастанию цены за м²
cheapest_per_m2 = df.sort_values(by="Цена_за_м2").head(5)
# Выводим
print_df('💰 ТОП самых ДЕШЕВЫХ объектов по цене за м²', cheapest_per_m2)


#                      Выводим ТОП-5 самых дорогих
# Сортируем по убыванию цены за м²
most_expensive_per_m2 = df.sort_values(by="Цена_за_м2", ascending=False).head(5)
# Выводим
print_df('💰 ТОП самых ДОРОГИХ объектов по цене за м²', cheapest_per_m2)

    
#                   Отфильтровать объявления по условиям:
# Фильтрация
filtered_df = df[
    (df["Тип"] == "Продажа квартиры в новостройке") &
    (df["Цена_число"] <= 20_000_000) &
    (df["Площадь"] >= 40) &
    (df["Площадь"] <= 100)
]
print()
print(f"📊 Найдено подходящих объявлений: {len(filtered_df)}")
print_df('📊 ВОТ СПИСОК: ', filtered_df)


# Посчитать сколько квартир рядом со станцией водный стадион
vodny_count = filtered_df[filtered_df["Метро"].str.contains("м. Водный стадион", case=False)].shape[0]
print()
print(f"🚇 Квартир у метро «м. Водный стадион»: {vodny_count}")

# Группируем и считаем количество квартир по каждой станции метро
metro_counts = df["Метро"].value_counts()

# Выводим красиво
print()
print("🚇 Количество квартир по станциям метро:\n")
for metro, count in metro_counts.items():
    print(f"Станция метро: {metro} — {count} квартир")


# Группируем по станции метро и считаем среднюю цену за м²
metro_avg_price_per_m2 = (
    df.groupby("Метро")["Цена_за_м2"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
)

# Красивый вывод
print("\n\n💸 ТОП-10 станций метро по средней цене за м²:\n")
for metro, avg_m2_price in metro_avg_price_per_m2.items():
    print(f"{metro:<45} — {avg_m2_price:,.0f} ₽/м²")