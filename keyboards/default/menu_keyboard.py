from aiogram import types

menu_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
client_button = types.KeyboardButton("🙋‍♂️ Клиент")
profi_button = types.KeyboardButton("👨‍💻 Специалист")
about_button = types.KeyboardButton("ℹ О боте")


menu_keyboard.add(client_button, profi_button)
menu_keyboard.add(about_button)