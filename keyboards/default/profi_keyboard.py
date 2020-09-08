from aiogram import types

profi_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
bio_button = types.KeyboardButton("Расскажи о себе 👀")
edit_categories_button = types.KeyboardButton("Выбери категорию 📋")
hourly_rate_button = types.KeyboardButton("Средний чек за проект 💵")
portfolio_button = types.KeyboardButton("Портфолио 💼")
back_button = types.KeyboardButton("⬅️ Назад")
status_button = types.KeyboardButton("Статус ✅")


profi_keyboard.add(bio_button,edit_categories_button)
profi_keyboard.add(hourly_rate_button,portfolio_button)
profi_keyboard.add(back_button,status_button)