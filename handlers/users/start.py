from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from asyncpg import UniqueViolationError

from keyboards.default import menu_keyboard
from loader import dp
from utils.db_api.db_commands import add_freelancer, update_freelancer_name


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(f'Привет, {message.from_user.full_name}!', reply_markup=menu_keyboard)
