from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

delete_cd = CallbackData("delete_task", "id", "result")


async def delete_keyboard(id):
    markup = InlineKeyboardMarkup(row_width=2)
    button_text = "❌ Удалить"
    callback_data = delete_cd.new(id=id,result="scd")
    markup.insert(
        InlineKeyboardButton(text=button_text, callback_data=callback_data)
    )
    button_text = "✅ Заказ выполнен успешно!"
    callback_data = delete_cd.new(id=id, result="scc")
    markup.insert(
        InlineKeyboardButton(text=button_text, callback_data=callback_data)
    )
    return markup
