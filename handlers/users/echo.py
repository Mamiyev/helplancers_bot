from aiogram import types

from loader import dp


@dp.message_handler()
async def echo(message: types.Message):
    text = "Обработчик для данной комманды не задан\n Этот хендлер должен убираться при залитии на Production"
    await message.answer(text)
