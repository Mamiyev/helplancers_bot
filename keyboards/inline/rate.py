from aiogram import types
from aiogram.utils.callback_data import CallbackData

rate_cd = CallbackData("rate","number_of_days","sum_to_pay","information")

rate_keyboard = types.InlineKeyboardMarkup(row_width=1)
true_button = types.InlineKeyboardButton(text="💵Тру Хелпер за 390 рублей (15 дней)", callback_data="15:390:topay")
vip_button = types.InlineKeyboardButton(text="💵Вип Хелпер 790 рублей(30 дней)", callback_data="30:790:topay")
premium_button = types.InlineKeyboardButton(text="💵Премиум Хелпер 1490 рублей (90 дней)", callback_data="90:1490:topay")

rate_keyboard.add(true_button)
rate_keyboard.add(vip_button)
rate_keyboard.add(premium_button)
