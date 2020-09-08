import datetime
from aiogram import types
from typing import Union
from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from aiogram.utils.markdown import hlink, hcode
from asyncpg import UniqueViolationError

from data import config
from keyboards.inline import rate_keyboard
from keyboards.inline.menu_keyboard_profi import categories_keyboard, subcategories_keyboard, menu_cd, last_keyboard
from keyboards.inline.paid_keyboard import paid_keyboard
from loader import dp, bot
from aiogram.types import CallbackQuery
from keyboards.default import profi_keyboard

from states.profi_states import Profile, Freelancer as F
from utils.db_api.db_commands import update_freelancer_categories, update_freelancer_bio, \
    update_freelancer_github, update_freelancer_rate, \
    add_freelancer_subscription, update_freelancer_subscription, get_freelancer, \
    get_latest_freelancer_subscription, get_task, get_client
from utils.db_api.schemas.Freelancer_ import Freelancer_
from utils.misc.Qiwi import Payment, NoPaymentFound, NotEnoughMoney


@dp.callback_query_handler(text_contains="freed")  # Хендлер для кнопки Пробный период
async def profi(call: CallbackQuery):
    await call.answer(cache_time=60)
    await call.message.answer(text="👋Добро пожаловать!\n\n"
                                   "👨‍💻Это профиль фрилансера, где ты должен добавить информацию о себе используя"
                                   "кнопки ниже.\n💁‍♂️Выбери категории которые тебе интересны, а также укажи стоимость часа"
                                   "работы. Не забудь прикрепить свои работы, ведь твой профиль будут просматривать заказчики",
                              reply_markup=profi_keyboard)
    await call.message.delete()

    # об оформлении подписки
    today = datetime.date.today()
    now = datetime.datetime.now()
    current_time = datetime.time(now.hour, now.minute, now.second)

    start_time = datetime.datetime.combine(today, current_time)
    print(start_time)
    print(f"Время начала подписки: {start_time}")
    id = call.from_user.id
    print(id)
    subscription = datetime.timedelta(days=31)

    end_time = start_time + subscription
    print(f"Время окончание подписки: {end_time}")
    subscription = await get_latest_freelancer_subscription(call.from_user.id)
    if subscription.free_trial:
        await update_freelancer_subscription(start_date=start_time, end_date=end_time,
                                             freelancer_id=id, free_trial=False)
    else:
        await call.message.answer("Ваша пробная подписка уже была использована, необходимо преобрести новую:\n\n"
                                  "💶Тру Хелпер 390 рублей - 15 дней \n"
                                  "💶Вип Хелпер  790 рублей - 30 дней \n"
                                  "💶Премиум Хелпер 1490 рублей - 90 дней",
                                  reply_markup=rate_keyboard)
    print("Profi handler is executed")


@dp.callback_query_handler(text_contains="notfree")  # Хендлер для кнопки Платная подписка
async def subsc(call: CallbackQuery):
    await call.answer(cache_time=60)
    await call.message.answer(text="Выберите, пожалуйста, тариф \n\n"
                                   "💶Тру Хелпер 390 рублей - 15 дней \n\n"
                                   "💶Вип Хелпер  790 рублей - 30 дней \n\n"
                                   "💶Премиум Хелпер 1490 рублей - 90 дней",
                              reply_markup=rate_keyboard)


@dp.callback_query_handler(text_contains="topay")
async def paid_subscription(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=60)

    id = call.message.from_user.id
    days = call.data.split(":")[0]
    sum_to_pay = call.data.split(":")[1]

    payment = Payment(amount=sum_to_pay)
    payment.create()

    markup = await paid_keyboard(id=id, days=days)

    await call.message.edit_text(
        "\n".join(
            [
                f"Оплатите не менее {sum_to_pay} по номеру телефона или по адресу",
                "",
                hlink(config.WALLET_QIWI, url=payment.invoice),
                "И обязательно укажите ID платежа",
                hcode(payment.id)
            ]
        ),
        reply_markup=markup
    )
    await state.set_state("qiwi")
    await state.update_data(payment=payment)
    print("Subsc handler is executed")


@dp.callback_query_handler(text_contains="cancel_paid", state="qiwi")
async def cancel_payment(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text("Вы отменили покупку")
    await state.finish()


@dp.callback_query_handler(text="confirm_paid", state="qiwi")
async def confirm_payment(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    id = call.data.split(":")[-2]
    days = call.data.split(":")[-1]

    payment: Payment = data.get("payment")
    try:
        payment.check_payment()
    except NoPaymentFound:
        await call.message.answer("Транзакция не найдена")
        await state.finish()
        return
    except NotEnoughMoney:
        await call.message.answer("Оплаченная сумма меньше необходимой!")
        await state.finish()
        return
    else:
        await call.message.answer("Подписка успешно оплачена")

    # добавление ФРИЛАНСЕРА в таблицу у которых есть подписка
    today = datetime.date.today()
    now = datetime.datetime.now()
    current_time = datetime.time(now.hour, now.minute, now.second)

    start_time = datetime.datetime.combine(today, current_time)
    print(start_time)
    print(f"Время начала подписки: {start_time}")

    subscription = datetime.timedelta(days)

    end_time = start_time + subscription
    print(f"Время окончание подписки: {end_time}")

    try:
        await add_freelancer_subscription(freelancer_id=id, free_trial=False)
    except:
        await update_freelancer_subscription(start_date=start_time, end_date=end_time,
                                             freelancer_id=call.message.from_user.id)

    await call.message.delete_reply_markup()
    await call.message.answer(f"Ваша подписка действительна до: {end_time}")
    await state.finish()


@dp.message_handler(text_contains="Расскажи о себе 👀", state=None)
async def enter_test(message: types.Message):
    await message.answer("Добавьте информацию о себе.\n"
                         "Например:\n"
                         "Иван Иванов - front-end разработчик. Опыт 3 года\n"
                         "Навыки: HTML, CSS, JS, PYTHON")

    await Profile.about.set()


@dp.message_handler(state=Profile.about)
async def answer_q1(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(answer1=answer)

    await message.answer("Добавлено!\n"
                         "Перейдите к следующему пункту", reply_markup=profi_keyboard)
    await update_freelancer_bio(id=message.chat.id, bio=answer)
    await state.reset_state(with_data=False)


@dp.message_handler(text="Выбери категорию 📋")
async def pshow_menu(message: types.Message):
    await plist_categories(message)


async def plist_categories(message: Union[CallbackQuery, Message], **kwargs):
    markup = await categories_keyboard()

    # Проверяем, что за тип апдейта. Если Message - отправляем новое сообщение
    if isinstance(message, Message):
        await message.answer("Выберите категорию", reply_markup=markup)

    # Если CallbackQuery - изменяем это сообщение
    elif isinstance(message, CallbackQuery):
        call = message
        await call.message.edit_reply_markup(markup)


async def plist_subcategories(callback: CallbackQuery, category, **kwargs):
    markup = await subcategories_keyboard(category)
    await callback.message.edit_reply_markup(markup)


async def show_category_subcategory(callback: CallbackQuery, category, subcategory):
    id = callback.from_user.id
    await update_freelancer_categories(id=callback.message.chat.id,
                                       category_code=category, subcategory_code=subcategory)

    freelancer = await Freelancer_.get(id)
    text = f"""Выбранные категории: {freelancer.category_name}
Выбранные подкатегории: {freelancer.subcategory_name}
        """
    await callback.message.edit_text(text=text)


@dp.callback_query_handler(menu_cd.filter())
async def navigate(call: types.CallbackQuery, callback_data: dict):
    current_level = callback_data.get("level")
    category = callback_data.get("category")
    subcategory = callback_data.get("subcategory")

    levels = {
        "0": plist_categories,
        "1": plist_subcategories,
        "2": show_category_subcategory
    }
    if current_level == 2:
        current_level_function = levels[current_level]
        await F.finality.set()
        await current_level_function(call, category=category, subcategory=subcategory)
    else:
        current_level_function = levels[current_level]
        await current_level_function(call, category=category, subcategory=subcategory)


@dp.message_handler(text="Портфолио 💼")
async def insert_portfolio(message: types.Message):
    await message.answer("Введите свою ссылку на гитхаб аккаунт:")
    await Profile.github.set()


@dp.message_handler(state=Profile.github)
async def answer_q2(message: types.Message, state: FSMContext):
    link = message.text
    await state.update_data(github_link=link)

    await message.answer("Добавлено!\n"
                         "Перейдите к следующему пункту", reply_markup=profi_keyboard)
    await update_freelancer_github(id=message.chat.id, github=link)
    await state.reset_state(with_data=False)


@dp.message_handler(text="Средний чек за проект 💵")
async def insert_average_salary(message: types.Message):
    await message.answer("Введите свой средний чек за проект (ЕВРО)")
    await Profile.hourly_rate.set()


@dp.message_handler(state=Profile.hourly_rate)
async def answer_q2(message: types.Message, state: FSMContext):
    rate = int(message.text)
    await state.update_data(average_rate=rate)
    await message.answer("Добавлено!\n"
                         "Перейдите к следующему пункту", reply_markup=profi_keyboard)
    await update_freelancer_rate(id=message.chat.id, hourly_rate=rate)
    await state.reset_state(with_data=False)


@dp.message_handler(text="Статус ✅")
async def show_repr(message: types.Message):
    freelancer = await Freelancer_.get(message.from_user.id)
    text = freelancer.__repr__()
    if freelancer.name != 'Null':
        if freelancer.category_code != 'Null':
            if freelancer.subcategory_code != 'Null':
                if freelancer.bio != 'Null':
                    if freelancer.average_salary != 'Null':
                        if freelancer.github != 'Null':
                            text += '\n✅Все поля заполнены '
                        else:
                            text += '\n🛑Не все поля заполнены'
                    else:
                        text += '\n🛑Не все поля заполнены'
                else:
                    text += '\n🛑Не все поля заполнены'
            else:
                text += '\n🛑Не все поля заполнены'
        else:
            text += '\n🛑Не все поля заполнены'
    else:
        text += '\n🛑Не все поля заполнены'

    await message.answer(text)


@dp.message_handler(state=F.finality)
async def finall(state: FSMContext):
    await state.finish()


@dp.callback_query_handler(menu_cd.filter())
async def navigate(call: types.CallbackQuery, callback_data: dict):
    current_level = callback_data.get("level")
    category = callback_data.get("category")
    subcategory = callback_data.get("subcategory")

    levels = {
        "0": plist_categories,
        "1": plist_subcategories,
        "2": show_category_subcategory
    }
    if current_level == 2:
        current_level_function = levels[current_level]
        await F.finality.set()
        await current_level_function(call, category=category, subcategory=subcategory)
    else:
        current_level_function = levels[current_level]
        await current_level_function(call, category=category, subcategory=subcategory)


# когда пришло сообщение о заказе - может нажать на него что бы посмотреть на username заказчика
@dp.callback_query_handler(text_contains="gtff")
async def get_task_from_freelancer(call: CallbackQuery):
    subscription_of_freelancer = await get_latest_freelancer_subscription(call.from_user.id)
    freelancer = await get_freelancer(call.from_user.id)
    task_id = int(call.data.split(":")[-1])
    task = await get_task(task_id)

    client = await get_client(task.client_id)

    text = str(task.__repr__()) + f"\n@{client.username}"

    today = datetime.date.today()
    now = datetime.datetime.now()
    current_time = datetime.time(now.hour, now.minute, now.second)
    now_time = datetime.datetime.combine(today, current_time)

    text_for_client = "😉Ваш заказ посмотрел исполнитель:\n" + freelancer.__repr__() + f"\n@{freelancer.name}"
    # если подписка действительна:
    if subscription_of_freelancer.end_date > now_time:
        await call.message.answer(text=text)
        await bot.send_message(chat_id=client.id, text=text_for_client)
    else:
        await call.message.answer(
            text="У вас нет активной подписки. Вам стоит обновить её", reply_markup=rate_keyboard)
