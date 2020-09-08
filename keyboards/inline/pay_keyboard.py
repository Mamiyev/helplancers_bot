from aiogram.types import InlineKeyboardButton


def pay_subscription(sum_to_pay,days):
     keyboard = InlineKeyboardButton(
         inline_keyboard=[
             [
                 InlineKeyboardButton(text = f"Купить подписку на {days} дней",
                                      callback_data=f"buy:{days}")
             ]
         ]
     )
     return keyboard