import matplotlib.pyplot as plt
from io import BytesIO
import locale
from datetime import datetime

locale.setlocale(locale.LC_TIME, "ru_RU.UTF-8")

def format_date(date_str):
    """Преобразует дату из ISO-формата в читабельный формат"""
    date = datetime.strptime(date_str[:10], "%Y-%m-%d")
    return date.strftime("%d %B")

def create_combined_temperature_plot(city1_data, city2_data, city1_name, city2_name):
    """Создает комбинированный график температуры для двух городов."""
    dates = [format_date(entry['date']) for entry in city1_data]
    temps_city1_max = [entry['temperature_max'] for entry in city1_data]
    temps_city1_min = [entry['temperature_min'] for entry in city1_data]
    temps_city2_max = [entry['temperature_max'] for entry in city2_data]
    temps_city2_min = [entry['temperature_min'] for entry in city2_data]

    plt.figure(figsize=(12, 6))
    plt.plot(dates, temps_city1_max, label=f'{city1_name} Макс', marker='o', color='red')
    plt.plot(dates, temps_city1_min, label=f'{city1_name} Мин', marker='o', color='orange')
    plt.plot(dates, temps_city2_max, label=f'{city2_name} Макс', marker='o', color='blue')
    plt.plot(dates, temps_city2_min, label=f'{city2_name} Мин', marker='o', color='cyan')
    plt.fill_between(dates, temps_city1_min, temps_city1_max, color='red', alpha=0.2, label=f'{city1_name} Диапазон')
    plt.fill_between(dates, temps_city2_min, temps_city2_max, color='blue', alpha=0.2, label=f'{city2_name} Диапазон')

    plt.title('Сравнение температур для двух городов', fontsize=16)
    plt.xlabel('Дата', fontsize=12)
    plt.ylabel('Температура (°C)', fontsize=12)
    plt.legend()
    plt.grid()

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()
    return buffer

def create_combined_humidity_plot(city1_data, city2_data, city1_name, city2_name):
    """Создает комбинированный график влажности для двух городов."""
    dates = [format_date(entry['date']) for entry in city1_data]
    humidity_city1 = [entry['humidity'] for entry in city1_data]
    humidity_city2 = [entry['humidity'] for entry in city2_data]

    plt.figure(figsize=(12, 6))
    plt.plot(dates, humidity_city1, label=f'{city1_name}', marker='o', color='purple')
    plt.plot(dates, humidity_city2, label=f'{city2_name}', marker='o', color='blue')
    plt.title('Сравнение влажности для двух городов', fontsize=16)
    plt.xlabel('Дата', fontsize=12)
    plt.ylabel('Влажность (%)', fontsize=12)
    plt.legend()
    plt.grid()

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()
    return buffer

def create_combined_rainfall_plot(city1_data, city2_data, city1_name, city2_name):
    """Создает комбинированный график осадков для двух городов."""
    dates = [format_date(entry['date']) for entry in city1_data]
    rain_prob_city1 = [entry['rain_probability'] for entry in city1_data]
    rain_prob_city2 = [entry['rain_probability'] for entry in city2_data]

    plt.figure(figsize=(12, 6))
    plt.plot(dates, rain_prob_city1, label=f'{city1_name}', marker='o', color='cyan')
    plt.plot(dates, rain_prob_city2, label=f'{city2_name}', marker='o', color='blue')
    plt.title('Сравнение вероятности осадков для двух городов', fontsize=16)
    plt.xlabel('Дата', fontsize=12)
    plt.ylabel('Вероятность осадков (%)', fontsize=12)
    plt.legend()
    plt.grid()

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()
    return buffer

def create_humidity_plot(data, city_name):
    """Создает график влажности для одного города."""
    dates = [format_date(entry['date']) for entry in data]
    humidity = [entry['humidity'] for entry in data]

    plt.figure(figsize=(10, 5))
    plt.bar(dates, humidity, color='purple', alpha=0.7)
    plt.title(f'Влажность в {city_name}', fontsize=16)
    plt.xlabel('Дата', fontsize=12)
    plt.ylabel('Влажность (%)', fontsize=12)
    plt.grid(axis="y")

    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    plt.close()
    return buffer

def create_rainfall_plot(data, city_name):
    """Создает график вероятности осадков для одного города."""
    dates = [format_date(entry['date']) for entry in data]
    rain_prob = [entry['rain_probability'] for entry in data]

    plt.figure(figsize=(10, 5))
    plt.bar(dates, rain_prob, color='blue', alpha=0.7)
    plt.title(f'Вероятность осадков в {city_name}', fontsize=16)
    plt.xlabel("Дата", fontsize=12)
    plt.ylabel("Вероятность (%)", fontsize=12)
    plt.grid(axis="y")

    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    plt.close()
    return buffer
