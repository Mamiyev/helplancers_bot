from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

async def mailing_markup(task_id):
    mailing_message = InlineKeyboardMarkup(row_width=1,
                                           inline_keyboard=[
                                               [
                                                   InlineKeyboardButton(
                                                       text="🙌Получить информацию о заказчике",
                                                       # gtff = get task for freelancer
                                                       callback_data=f"gtff:{task_id}"
                                                   )
                                               ]
                                           ])
    return mailing_message
