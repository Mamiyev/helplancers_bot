from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

async def paid_keyboard(id,days):
    paid_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Оплатил", callback_data=f"confirm_paid:{id}:{days}")
            ],
            [
                InlineKeyboardButton(text="Отмена", callback_data=f"cancel_paid:{id}:{days}")
            ]
        ]
    )
    return paid_keyboard
