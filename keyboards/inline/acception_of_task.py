from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

accept_cd = CallbackData("accept_task", "id", "result", "find")


async def acception_keyboard(id):
    markup = InlineKeyboardMarkup(row_width=2)
    button_text = "✅"
    callback_data = f"{id}:True:acception"
    markup.insert(
        InlineKeyboardButton(text=button_text, callback_data=callback_data)
    )

    button_text = "⛔️"
    callback_data = f"{id}:False:acception"
    markup.insert(
        InlineKeyboardButton(text=button_text, callback_data=callback_data)
    )
    return markup
