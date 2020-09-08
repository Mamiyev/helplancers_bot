from aiogram import types

client_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
find_profi_button = types.KeyboardButton("🕵 Найти исполнителя")
back_button = types.KeyboardButton("⬅️ Назад")
my_works_button = types.KeyboardButton("📂 Мои заказы")


client_keyboard.add(find_profi_button)
client_keyboard.add(back_button, my_works_button)