from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_inline_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Подтвердить", callback_data="confirm")],
        [InlineKeyboardButton(text="Отмена", callback_data="cancel")]
    ])
    return keyboard

def get_days_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="1 день", callback_data="1")],
        [InlineKeyboardButton(text="3 дня", callback_data="3")],
        [InlineKeyboardButton(text="5 дней", callback_data="5")]
    ])
    return keyboard

def get_location_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📍 Отправить геолокацию", request_location=True)],
        [InlineKeyboardButton(text="🚫 Отмена", callback_data="cancel")]
    ])
    return keyboard
