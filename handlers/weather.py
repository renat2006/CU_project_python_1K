from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from api.weather_api import WeatherAPI
from keyboards.inline import get_inline_keyboard, get_days_keyboard
from data.config import WEATHER_API_KEY, LANGUAGE
from visualizations.plot import (
    create_combined_temperature_plot,
    create_combined_humidity_plot,
    create_combined_rainfall_plot,
)
from aiogram.types.input_file import BufferedInputFile
from datetime import datetime
import locale

locale.setlocale(locale.LC_TIME, "ru_RU.UTF-8")

router = Router()
weather_api = WeatherAPI(api_key=WEATHER_API_KEY, language=LANGUAGE)

class WeatherFSM(StatesGroup):
    start_location = State()
    end_location = State()
    days_selection = State()
    confirm_route = State()

def format_date(date_str):
    """Преобразует дату из ISO-формата в читабельный формат."""
    date = datetime.strptime(date_str[:10], "%Y-%m-%d")
    return date.strftime("%d %B")

def format_forecast(data, city_name):
    """Форматирует текстовый прогноз погоды."""
    forecast_text = f"📍 Погода для города: {city_name}\n"
    for day in data:
        date = format_date(day['date'])
        forecast_text += (
            f"📅 {date}:\n"
            f"🌡️ Макс: {day['temperature_max']}°C | Мин: {day['temperature_min']}°C\n"
            f"💧 Влажность: {day['humidity']}%\n"
            f"💨 Ветер: {day['wind_speed']} км/ч\n"
            f"☔ Дождь: {day['rain_probability']}%\n\n"
        )
    return forecast_text

@router.message(Command("weather"))
async def cmd_weather(message: types.Message, state: FSMContext):
    await message.answer("Введите начальную точку маршрута 🏁:")
    await state.set_state(WeatherFSM.start_location)

@router.message(WeatherFSM.start_location)
async def process_start_location(message: types.Message, state: FSMContext):
    await state.update_data(start_location=message.text)
    await message.answer("Введите конечную точку маршрута 🎯:")
    await state.set_state(WeatherFSM.end_location)

@router.message(WeatherFSM.end_location)
async def process_end_location(message: types.Message, state: FSMContext):
    await state.update_data(end_location=message.text)
    await message.answer(
        "На сколько дней хотите получить прогноз? (1-5 дней) 📅",
        reply_markup=get_days_keyboard()
    )
    await state.set_state(WeatherFSM.days_selection)

@router.callback_query(lambda call: call.data.isdigit())
async def select_days(call: types.CallbackQuery, state: FSMContext):
    days = int(call.data)
    await state.update_data(days=days)
    data = await state.get_data()
    start = data['start_location']
    end = data['end_location']
    await call.message.answer(
        f"🌍 Ваш маршрут:\n"
        f"🔹 Начало: <b>{start}</b>\n"
        f"🔹 Конец: <b>{end}</b>\n"
        f"🔹 Прогноз на: <b>{days} дней</b>\n\n"
        f"✅ Нажмите 'Подтвердить' для продолжения.",
        reply_markup=get_inline_keyboard(),
        parse_mode="HTML"
    )
    await state.set_state(WeatherFSM.confirm_route)

@router.callback_query(lambda call: call.data == "confirm")
async def confirm_route(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    start_city = data['start_location']
    end_city = data['end_location']
    days = data['days']

    try:

        start_autocomplete = await weather_api.get_cities_autocomplete(start_city)
        end_autocomplete = await weather_api.get_cities_autocomplete(end_city)

        if not start_autocomplete or not end_autocomplete:
            await call.message.answer("Не удалось найти указанные города. Попробуйте снова.")
            return

        start_location_key = start_autocomplete[0]['Key']
        end_location_key = end_autocomplete[0]['Key']

        start_forecast = await weather_api.get_forecast_daily(5, start_location_key)
        end_forecast = await weather_api.get_forecast_daily(5, end_location_key)

        start_forecast = start_forecast[:days]
        end_forecast = end_forecast[:days]

        start_text = format_forecast(start_forecast, start_city)
        end_text = format_forecast(end_forecast, end_city)

        combined_temp_plot = create_combined_temperature_plot(
            start_forecast, end_forecast, start_city, end_city
        )
        combined_humidity_plot = create_combined_humidity_plot(
            start_forecast, end_forecast, start_city, end_city
        )
        combined_rainfall_plot = create_combined_rainfall_plot(
            start_forecast, end_forecast, start_city, end_city
        )

        combined_temp_file = BufferedInputFile(combined_temp_plot.getvalue(), filename="combined_temp.png")
        combined_humidity_file = BufferedInputFile(combined_humidity_plot.getvalue(), filename="combined_humidity.png")
        combined_rainfall_file = BufferedInputFile(combined_rainfall_plot.getvalue(), filename="combined_rainfall.png")

        await call.message.answer_photo(photo=combined_temp_file, caption="🌡️ Сравнительный график температуры")
        await call.message.answer_photo(photo=combined_humidity_file, caption="💧 Сравнительный график влажности")
        await call.message.answer_photo(photo=combined_rainfall_file, caption="☔ Сравнительный график осадков")
        await call.message.answer(f"{start_text}\n{end_text}", parse_mode="HTML")
    except Exception as e:
        await call.message.answer(f"❌ Ошибка: {e}")
    finally:
        await state.clear()

@router.message()
async def unknown_command(message: types.Message):
    """Обработчик неизвестных команд."""
    await message.answer(
        "⚠️ Я не понимаю эту команду. Вот что я могу:\n\n"
        "📌 <b>Доступные команды:</b>\n"
        "• /weather — Получить прогноз погоды\n"
        "• /help — Получить помощь\n\n"
        "Попробуйте еще раз! 😊",
        parse_mode="HTML"
    )
