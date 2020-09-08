from aiogram import types

quiz_keyboard = types.InlineKeyboardMarkup(row_width=1)
free_button = types.InlineKeyboardButton(text="Пробный период", callback_data="freed")
subs_button = types.InlineKeyboardButton(text="💰Платная подписка", callback_data="notfree")
quiz_keyboard.add(free_button, subs_button)



