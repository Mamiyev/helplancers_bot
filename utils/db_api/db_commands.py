from typing import List

from sqlalchemy import and_

from utils.db_api.database import db
from utils.db_api.schemas.Task_ import Client_
from utils.db_api.schemas.Freelancer_ import Freelancer_, Subscription_
from utils.db_api.schemas.Task_ import Task_


# Фукнкции для задания

async def add_task(**kwargs):
    newtask = await Task_(**kwargs).create()
    return newtask


async def update_task_subcategory_code(id, subcategory_code):
    task = await Task_.get(id)
    await task.update(subcategory_code=subcategory_code).apply()


async def update_task_category_name(id, category_name):
    task = await Task_.get(id)
    await task.update(category_name=category_name).apply()


async def update_task_subcategory_name(id, subcategory_name):
    task = await Task_.get(id)
    await task.update(subcategory_name=subcategory_name).apply()


async def update_task_description(id, description):
    task = await Task_.get(id)
    await task.update(description=description).apply()


async def update_task_salary(id, salary):
    task = await Task_.get(id)
    await task.update(salary=salary).apply()


async def add_freelancer_subscription(**kwargs):
    newfreelancer_subscription = await Subscription_(**kwargs).create()
    return newfreelancer_subscription


async def update_freelancer_subscription(freelancer_id, start_date, end_date, free_trial=True):
    subscription = await get_latest_freelancer_subscription(freelancer_id)
    await subscription.update(start_date=start_date, end_date=end_date).apply()
    if free_trial:
        pass
    else:
        await subscription.update(free_trial=False).apply()


async def update_task_category_code(id, category_code):
    task = await get_task(id)
    await task.update(category_code=category_code).apply()


async def get_categories() -> List[Task_]:
    # проверять на "0" и на нулл
    lists = await Task_.query.distinct(Task_.category_name).gino.all()
    print(lists)
    return lists



async def update_client_name(client_id,name):
    client = await get_client(client_id)
    await client.update(username=name).apply()

async def get_subcategories(category_code) -> List[Task_]:
    return await Task_.query.distinct(Task_.subcategory_code).where(Task_.category_code == category_code).gino.all()


async def count_finished_projects(status=True):
    total = await db.select([db.func.count()]).where(
        Task_.status == status
    ).gino.scalar()
    return total


# Функция для получения всех ТАСКОВ
async def get_all_tasks() -> List[Task_]:
    tasks = await Task_.query.where(Task_.client_id != 0).gino.all()
    return tasks


async def get_all_my_tasks(client_id) -> List[Task_]:
    tasks = await Task_.query.where(Task_.client_id == client_id).gino.all()
    return tasks


# Функция для админки. Выводит все заказы с определённой категорией и подкатегорией
async def get_tasks(category_code, subcategory_code) -> List[Task_]:
    tasks = await Task_.query.where(
        and_(Task_.category_code == category_code, Task_.subcategory_code == subcategory_code)
    ).gino.all()
    return tasks


# Функция для вывода информации по ТАСКУ по его ID
async def get_task(task_id) -> Task_:
    task = await Task_.query.where(Task_.id == task_id).gino.first()
    return task


async def count_tasks():
    total = await db.select([db.func.count()]).where(
        Task_.id != None
    ).gino.scalar()
    return total


async def count_next_task_id():
    tasks = await Task_.query.order_by(Task_.created_at.desc()).gino.first()
    return tasks.id

async def update_current_task(id, current_task_id):
    client = await get_client(id)
    await client.update(current_task_id=current_task_id).apply()


async def delete_task(id):
    task = await get_task(id)
    await task.delete()


async def finish_task(id):
    task = await get_task(id)
    await task.update(status=True).apply()


# ФУНКЦИИ ДЛЯ РАБОТЫ С ФРИЛАНСЕРОМ
async def add_freelancer(**kwargs):
    newfreelancer = await Freelancer_(**kwargs).create()
    return newfreelancer


async def add_subscription(**kwargs):
    newsubscription = await Subscription_(**kwargs).create()
    return newsubscription


# Обновления для пользователя в базу данных
async def update_freelancer_name(id, name):
    freelancer = await Freelancer_.get(id)
    await freelancer.update(name=name).apply()


async def get_freelancers() -> List[Freelancer_]:
    freelancers = await Freelancer_.query.where(
        Freelancer_.id >= 22
    ).gino.all()
    return freelancers


async def get_freelancer_subscription(freelancer_id) -> Subscription_:
    subscription = await Subscription_.query.where(
        Subscription_.freelancer_id == freelancer_id
    ).gino.first()
    return subscription


async def update_freelancer_categories(id, category_code, subcategory_code):
    # Тут обновим и имя категории\подкатегории
    # Обновления для категорий
    freelancer = await get_freelancer(id)
    if freelancer.category_code == "0":
        await freelancer.update(category_code=category_code).apply()
    else:
        prev_category_code = freelancer.category_code
        final_category_code = str(prev_category_code) + " " + str(category_code)
        await freelancer.update(category_code=final_category_code).apply()
    await update_freelancer_category_name_with_category_code(id, category_code=category_code)

    # Обновления для подкатегорий
    if freelancer.subcategory_code == "0":
        await freelancer.update(subcategory_code=subcategory_code).apply()
    else:
        prev_subcategory_code = freelancer.subcategory_code
        final_subcategory_code = str(prev_subcategory_code) + " " + str(subcategory_code)
        await freelancer.update(subcategory_code=final_subcategory_code).apply()
    await update_freelancer_subcategory_name_with_subcategory_code(id, subcategory_code)


async def update_freelancer_category_name_with_category_code(id, category_code):
    freelancer = await get_freelancer(id)
    if freelancer.subcategory_name:
        prev_category_name = freelancer.category_name
    else:
        prev_category_name = ""

    new_category_name = "0"
    if category_code == "design":
        new_category_name = "Дизайн"
    elif category_code == "other":
        new_category_name = "Другое"
    elif category_code == "dev":
        new_category_name = "Разработка"
    elif category_code == "copywr":
        new_category_name = "Копирайтинг"
    elif category_code == "marketing":
        new_category_name = "Маркетинг"

    if freelancer.category_name == "":
        await freelancer.update(category_name=new_category_name).apply()
    else:
        if prev_category_name == "":
            final_category_name = str(prev_category_name) + "" + str(new_category_name)
            await freelancer.update(category_name=final_category_name).apply()
        else:
            final_category_name = str(prev_category_name) + ", " + str(new_category_name)
            await freelancer.update(category_name=final_category_name).apply()


async def update_freelancer_subcategory_name_with_subcategory_code(id, subcategory_code):
    freelancer = await get_freelancer(id)
    if freelancer.subcategory_name:
        prev_subcategory_name = freelancer.subcategory_name
    else:
        prev_subcategory_name = ""
    new_subcategory_name = "0"

    # обновления для подкатегорий
    if subcategory_code == "web":
        new_subcategory_name = "Веб-дизай"
    if subcategory_code == "animation":
        new_subcategory_name = "Анимации"
    if subcategory_code == "logo":
        new_subcategory_name = "Логотипы"
    if subcategory_code == "illustration":
        new_subcategory_name = "Иллюстрации"
    if subcategory_code == "3d":
        new_subcategory_name = "3Д-моделирование"
    if subcategory_code == "inst":
        new_subcategory_name = "Инстаграм"
    if subcategory_code == "vk":
        new_subcategory_name = "ВК"
    if subcategory_code == "tg":
        new_subcategory_name = "Телеграм"
    if subcategory_code == "fb":
        new_subcategory_name = "Фейсбук"
    if subcategory_code == "seo":
        new_subcategory_name = "SEO-продвижение"
    if subcategory_code == "posts":
        new_subcategory_name = "Статьи"
    if subcategory_code == "translate":
        new_subcategory_name = "Переводы"
    if subcategory_code == "seotxt":
        new_subcategory_name = "SEO-тексты"
    if subcategory_code == "sellingtxt":
        new_subcategory_name = "Продающие тексты"
    if subcategory_code == "front":
        new_subcategory_name = "Front-end"
    if subcategory_code == "backend":
        new_subcategory_name = "Back-end"
    if subcategory_code == "game":
        new_subcategory_name = "Игры"
    if subcategory_code == "landing":
        new_subcategory_name = "Лендинг"
    if subcategory_code == "music":
        new_subcategory_name = "Музыка"
    if subcategory_code == "video":
        new_subcategory_name = "Видео"
    if subcategory_code == "photo":
        new_subcategory_name = "Фотографии"
    if subcategory_code == "tgbots":
        new_subcategory_name = "Телеграм боты"

    if freelancer.subcategory_name == "":
        await freelancer.update(subcategory_name=new_subcategory_name).apply()
    else:
        if prev_subcategory_name == "":
            final_subcategory_name = str(prev_subcategory_name) + "" + new_subcategory_name
            await freelancer.update(subcategory_name=final_subcategory_name).apply()
        else:
            final_subcategory_name = str(prev_subcategory_name) + ", " + new_subcategory_name
            await freelancer.update(subcategory_name=final_subcategory_name).apply()



async def update_freelancer_category_name(id, category_name):
    freelancer = await Freelancer_.get(id)
    await freelancer.update(category_name=category_name).apply()


async def update_freelancer_subcategory_name(id, subcategory_name):
    freelancer = await Freelancer_.get(id)
    await freelancer.update(subcategory_name=subcategory_name).apply()


async def update_freelancer_category_code(id, category_code):
    freelancer = await Freelancer_.get(id)
    await freelancer.update(category_code=category_code).apply()


async def update_freelancer_subcategory_code(id, subcategory_code):
    freelancer = await Freelancer_.get(id)
    await freelancer.update(subcategory_code=subcategory_code).apply()


async def update_freelancer_bio(id, bio):
    freelancer = await Freelancer_.get(id)
    await freelancer.update(bio=bio).apply()


async def update_freelancer_github(id, github):
    freelancer = await Freelancer_.get(id)
    await freelancer.update(github=github).apply()


async def update_freelancer_rate(id, hourly_rate):
    freelancer = await Freelancer_.get(id)
    await freelancer.update(average_salary=hourly_rate).apply()


async def count_freelancers(category_code, subcategory_code=None):
    conditions = [Freelancer_.category_code == category_code]

    if subcategory_code:
        conditions.append(Freelancer_.subcategory_code == subcategory_code)

    total = await db.select([db.func.count()]).where(
        and_(*conditions)
    ).gino.scalar()
    return total


# Функция для получени инфомрациио подписке ФРИЛАНСЕРА
async def get_latest_freelancer_subscription(freelancer_id) -> Subscription_:
    subscription = await Subscription_.query.where(Subscription_.freelancer_id == freelancer_id).gino.first()
    return subscription


# Функция для вывода информации по ФРИЛАНСЕРУ по его ID
async def get_freelancer(freelancer_id) -> Freelancer_:
    freelancer = await Freelancer_.query.where(Freelancer_.id == freelancer_id).gino.first()
    return freelancer


# ФУНКЦИИ ДЛЯ РАБОТЫ С КЛИЕНТОМ

async def add_client(**kwargs):
    newclient = await Client_(**kwargs).create()
    return newclient


async def get_client(client_id) -> Client_:
    client = await Client_.query.where(Client_.id == client_id).gino.first()
    return client


async def client_id_to_task_id(client_id) -> int:
    client = await get_client(client_id)
    id = client.current_task_id
    return id
