from aiogram import types
from aiogram.types import message

from loader import bot

from utils.db_api.database import create_db, db


async def on_startup(dp):
    import filters
    import middlewares
    filters.setup(dp)
    middlewares.setup(dp)
    await create_db()
    #await db.gino.drop_all()


    from utils.notify_admins import on_startup_notify
    await on_startup_notify(dp)


if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp

    executor.start_polling(dp, on_startup=on_startup)

