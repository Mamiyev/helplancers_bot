from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp
from utils.misc import rate_limit


@rate_limit(5, 'help')
@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    text = [
        'Список команд: ',
        '/start - Начать диалог',
        'Необходимо следовать инструкциям нашего бота, и внимательно читать\nчто от Вас просят😉 Хорошего Вам дня!'
    ]
    await message.answer('\n'.join(text))
