import datetime
from unittest.mock import call

from aiogram.dispatcher import FSMContext
from asyncpg import UniqueViolationError

from keyboards.inline.quiz import quiz_keyboard
from loader import dp

from keyboards.default import client_keyboard, menu_keyboard, profi_keyboard
from aiogram.types import Message

from utils.db_api.db_commands import add_freelancer, update_freelancer_name, count_finished_projects, add_client, \
    add_subscription, get_latest_freelancer_subscription, update_client_name


@dp.message_handler(text="👨‍💻 Специалист")  # Хендлер для кнопки Специалист
async def quiz(message: Message):
    subscription = await get_latest_freelancer_subscription(message.from_user.id)

    #Добавил проверку на наличие подписки
    try:
        if subscription.end_date:
            if subscription.end_date > datetime.datetime.now():
                await message.answer("Ваша подписка ещё действительна. Можете принимать заказы спокойно😁",
                                 reply_markup=profi_keyboard)
        else:
            markup = quiz_keyboard
            await message.answer(text="Небольшой опрос \n"
                                  "Платная подписка позволяет получать клиентов  "
                                  "приоритизированно на регулярной основне. \n"
                                  "Ознакомиться с тарифами можно начав на кнопку 'Платная подписка'",
                             reply_markup=markup)
            call.message.delete()
            try:
                await add_freelancer(id=message.from_user.id, name=message.from_user.username)
                await add_subscription(freelancer_id=message.from_user.id, free_trial=True)
            except UniqueViolationError:
                await update_client_name(client_id=message.from_user.id, name=message.from_user.username)
    except:
        markup = quiz_keyboard
        await message.answer(text="Небольшой опрос \n"
                                  "Платная подписка позволяет получать клиентов  "
                                  "приоритизированно на регулярной основне. \n"
                                  "Ознакомиться с тарифами можно начав на кнопку 'Платная подписка'",
                             reply_markup=markup)
        call.message.delete()
        try:
            await add_freelancer(id=message.from_user.id, name=message.from_user.username)
            await add_subscription(freelancer_id=message.from_user.id, free_trial=True)
        except UniqueViolationError:
            pass

    print("quiz handler is executed")


@dp.message_handler(text="🙋‍♂️ Клиент")  # Хендлер для кнопки Клиент
async def client(message: Message):
    await message.answer(text="Для поиска фрилансера нажмите на кнопку - 'Найти исполнителя'",
                         reply_markup=client_keyboard)

    try:
        if message.from_user.username is None:
            await message.answer("⚠️Предупреждение!\nВы не заполнили свой username в телеграмме\nДо того момента как Вы не заполните эту строку наши специалисты не смогут с Вами связаться")
        await add_client(id=message.from_user.id, username=message.from_user.username)
    except UniqueViolationError:
        await update_client_name(client_id=message.from_user.id, name = message.from_user.username)
    call.message.delete()
    print("client handler is executed")


@dp.message_handler(text="⬅️ Назад", state="*")  # Хендлер для кнопки Назад
async def back(message: Message,state:FSMContext = ""):

    await message.answer(text="Нажмите на 'Клиент' если хотите найти фрилансера  \n"
                         "Или на 'Специалист' если хотите брать заказы",
                         reply_markup=menu_keyboard)
    call.message.delete()
    await state.finish()
    print("back handler is executed")




@dp.message_handler(text="ℹ О боте")
async def about(message: Message):
    finished_projects = await count_finished_projects()
    await message.answer(text="Информация о боте\n"
                              f"Всего выполненных заказов: {finished_projects}\n",
                         reply_markup=menu_keyboard)
    call.message.delete()
    print("about handler is executed")
