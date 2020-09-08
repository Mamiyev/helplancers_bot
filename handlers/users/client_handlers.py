from typing import Union
from aiogram import types
from aiogram.dispatcher import FSMContext
from asyncpg import UniqueViolationError

from keyboards.inline.acception_of_task import acception_keyboard
from keyboards.inline.delete_task import delete_keyboard, delete_cd
from keyboards.inline.mailing_text import mailing_markup
from keyboards.inline.menu_keyboards_client import categories_keyboard, subcategories_keyboard, menu_cd
from aiogram.types import CallbackQuery
from loader import dp, bot
from states.steps_to_create_task import Task_state
from utils.db_api.db_commands import add_task, update_task_category_code, update_task_subcategory_code, \
    update_task_description, update_task_salary, update_task_category_name, update_task_subcategory_name, get_task, \
    count_tasks, update_current_task, client_id_to_task_id, delete_task, get_all_tasks, get_freelancers, \
    get_all_my_tasks, finish_task, get_client, count_next_task_id
from utils.db_api.schemas.Task_ import Task_


@dp.message_handler(text="🕵 Найти исполнителя")
async def show_menu(message: types.Message):
    id = message.from_user.id
    current_total_tasks = await count_next_task_id()
    await add_task(id=current_total_tasks + 1, client_id=id, category_code="0", subcategory_code="0",
                   category_name="0", subcategory_name="0")
    await update_current_task(id=id, current_task_id=current_total_tasks + 1)
    await Task_state.start.set()
    await list_categories(message)


async def list_categories(message: Union[types.Message, types.CallbackQuery], **kwargs):
    markup = await categories_keyboard()
    if isinstance(message, types.Message):
        await message.answer("Категории для твоего заказа:", reply_markup=markup)
    elif isinstance(message, types.CallbackQuery):
        call = message
        await call.message.edit_text(text="Категории для твоего заказа:", reply_markup=markup)
        id = await client_id_to_task_id(call.from_user.id)
        await update_task_category_code(id=id, category_code="0")


# навигатор по выдаче inline-кнопок
@dp.callback_query_handler(menu_cd.filter(), state=Task_state.start)
async def navigate(message: types.CallbackQuery, callback_data: dict):
    current_level = callback_data.get('level')
    category = callback_data.get('category')
    subcategory = callback_data.get('subcategory')
    id = await client_id_to_task_id(message.from_user.id)
    levels = {
        "0": list_categories,
        "1": list_subcategories,
    }
    if current_level == '0':
        current_level_function = levels[current_level]
        await current_level_function(message, category=category, subcategory=subcategory)
    if current_level == '1':
        await update_task_category_code(id=id, category_code=category)
        await list_subcategories(call=message, category=category, subcategory=subcategory)
    if current_level == '2':
        await update_task_subcategory_code(id=id, subcategory_code=subcategory)
        await description(message)


async def list_subcategories(call: types.CallbackQuery, category, **kwargs):
    markup = await subcategories_keyboard(category)
    await call.message.edit_text("Подкатегории для твоего заказа:", reply_markup=markup)


async def description(call: types.CallbackQuery):
    await call.message.edit_text(text="✍️Введите короткое описание задания:")
    await Task_state.salary.set()


# Обработчки для "ТЗ"
@dp.message_handler(state=Task_state.salary)
async def list_salary(message: types.Message):
    description = message.text
    id = client_id_to_task_id(message.from_user.id)
    await update_task_description(id=id, description=description)
    await message.answer("💰Введите приблизительную  цену($):")
    await Task_state.pre_finished.set()


# Обработчик для ставки на проект
@dp.message_handler(state=Task_state.pre_finished)
async def add_new_task(message: types.Message, state: FSMContext):
    id = await client_id_to_task_id(message.from_user.id)

    salary = int(message.text)
    await update_task_salary(id=id, salary=salary)
    task = await get_task(id)

    task_id = task.id
    category = task.category_code
    subcategory = task.subcategory_code
    client_id_freelancer = message.from_user.id

    await state.update_data(category_code=category, subcategory_code=subcategory,
                            id=client_id_freelancer, task_id=task_id)

    # тут заполняются category_name & subcategory_name
    if task.category_code == "design":
        await update_task_category_name(id=id, category_name="Дизайн")
        if task.subcategory_code == "web":
            await update_task_subcategory_name(id=id, subcategory_name="Веб-дизайн")
        elif task.subcategory_code == "animation":
            await update_task_subcategory_name(id=id, subcategory_name="Анимации")
        elif task.subcategory_code == "logo":
            await update_task_subcategory_name(id=id, subcategory_name="Логотипы")
        elif task.subcategory_code == "illustration":
            await update_task_subcategory_name(id=id, subcategory_name="Иллюстрации")
        elif task.subcategory_code == "3d":
            await update_task_subcategory_name(id=id, subcategory_name="3Д-моделирование")
    elif task.category_code == "marketing":
        await update_task_category_name(id=id, category_name="Маркетинг")
        if task.subcategory_code == "inst":
            await update_task_subcategory_name(id=id, subcategory_name="Инстаграм")
        elif task.subcategory_code == "vk":
            await update_task_subcategory_name(id=id, subcategory_name="ВКонтакте")
        elif task.subcategory_code == "tg":
            await update_task_subcategory_name(id=id, subcategory_name="Телеграмм")
        elif task.subcategory_code == "fb":
            await update_task_subcategory_name(id=id, subcategory_name="Фейсбук")
        elif task.subcategory_code == "seo":
            await update_task_subcategory_name(id=id, subcategory_name="SEO-продвижение")
    elif task.category_code == "copywr":
        await update_task_category_name(id=id, category_name="Копирайтинг")
        if task.subcategory_code == "posts":
            await update_task_subcategory_name(id=id, subcategory_name="Статьи")
        elif task.subcategory_code == "translate":
            await update_task_subcategory_name(id=id, subcategory_name="Переводы")
        elif task.subcategory_code == "seotxt":
            await update_task_subcategory_name(id=id, subcategory_name="SEO-тексты")
        elif task.subcategory_code == "sellingtxt":
            await update_task_subcategory_name(id=id, subcategory_name="Продающие тексты")
    elif task.category_code == "dev":
        await update_task_category_name(id=id, category_name="Разработка")
        if task.subcategory_code == "frontend":
            await update_task_subcategory_name(id=id, subcategory_name="Front-end")
        elif task.subcategory_code == "backend":
            await update_task_subcategory_name(id=id, subcategory_name="Back-end")
        elif task.subcategory_code == "game":
            await update_task_subcategory_name(id=id, subcategory_name="Игры")
        elif task.subcategory_code == "tgbots":
            await update_task_subcategory_name(id=id, subcategory_name="Телеграм боты")
        elif task.subcategory_code == "landing":
            await update_task_subcategory_name(id=id, subcategory_name="Лендинг")
    elif task.category_code == "other":
        await update_task_category_name(id=id, category_name="Другое")
        if task.subcategory_code == "music":
            await update_task_subcategory_name(id=id, subcategory_name="Музыка")
        elif task.subcategory_code == "video":
            await update_task_subcategory_name(id=id, subcategory_name="Видео")
        elif task.subcategory_code == "photo":
            await update_task_subcategory_name(id=id, subcategory_name="Фотографии")

    task = await Task_.get(id)
    text = task.__repr__()
    markup = await acception_keyboard(id)
    await message.answer(text='Нажмите на галочку для подтверждения')
    await message.answer(text=text, reply_markup=markup)
    await Task_state.finished.set()


@dp.callback_query_handler(text_contains="acception", state=Task_state.finished)
async def mailing(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=60)
    id = call.data.split(":")[0]
    result = call.data.split(":")[1]

    if result == "True":
        await call.message.edit_text(text="Ваш заказ успешно добавлен!👌")
    elif result == "False":
        await delete_task(int(id))
        await call.message.edit_text(text="Ваш заказ успешно удалён!👌")
    await Task_state.mailing.set()

    data = await state.get_data()
    category_code = data.get("category_code")

    # можно настроить что бы он отправлял только по подкатегориям
    # но я думаю если категории смежные, то фрилансер захочет получать полную рассылку по категориям
    # subcategory_code = data.get("subcategory_code")

    id = data.get("id")
    task_id = data.get("task_id")

    freelancers = await get_freelancers()
    for freelancer in freelancers:
        if category_code in str(freelancer.category_code):
            task = await get_task(task_id)
            text = task.__repr__()
            markup = await mailing_markup(task_id)
            # Поставить проверку что б заказчику не присылался свой зака
            try:
                # Проверка для того что бы бот не прислал сообщение самому заказчике
                if freelancer.id == call.from_user.id:
                    pass
                else:
                    await bot.send_message(chat_id=freelancer.id, text=text, reply_markup=markup)
            except:
                continue
        else:
            continue
    await state.finish()


@dp.message_handler(text="📂 Мои заказы")
async def show_task(message: types.Message):
    id = message.from_user.id
    task_id = await client_id_to_task_id(id)
    tasks = await get_all_my_tasks(message.from_user.id)
    flag = False
    if not tasks:
        await message.answer("😐Вы ещё не задали ни одного задания нашим специалистам")
    else:
        for task in tasks:
            if task.client_id == id:
                if task.status == True:
                    continue
                if task.category_code == "0":
                    continue
                if task.subcategory_code == "0":
                    continue
                if task.category_name == "0":
                    continue
                if task.subcategory_name == "0":
                    continue
                if task.description == "0":
                    continue
                if task.salary == "0":
                    continue
                flag = True
                markup = await delete_keyboard(task.id)
                await message.answer(text=task.__repr__(), reply_markup=markup)
        if not flag:
            await message.answer("😐Ваш список заданий пуст")


@dp.callback_query_handler(delete_cd.filter())
async def delete_showing_task(call: CallbackQuery, callback_data: dict):
    id = int(callback_data.get('id'))
    result = callback_data.get('result')
    if result == "scc":
        await finish_task(id)
        await call.message.edit_text(text="Заказ  завершён😄")
    else:
        await delete_task(id)
        await call.message.edit_text(text="Заказ  удалён😔")
