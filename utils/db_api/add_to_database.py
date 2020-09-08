from utils.db_api.db_commands import add_task, add_freelancer

import asyncio

from utils.db_api.database import create_db


# В тасках можно подставить подходящий пример для категории/подкатегории

async def add_tasks():
    await add_task(category_name="Дизайн", category_code="design",
                   subcategory_name="Веб-дизайн", subcategory_code="web",
                   description="Нужно сделать логотип в стиле монограммы",
                   salary=10, status=True)
    await add_task(category_name="Дизайн", category_code="design",
                   subcategory_name="Анимации", subcategory_code="animation",
                   description="Нужно сделать логотип в стиле монограммы",
                   salary=10, status=True)
    await add_task(category_name="Дизайн", category_code="design",
                   subcategory_name="Логотипы", subcategory_code="logo",
                   description="Нужно сделать логотип в стиле монограммы",
                   salary=10, status=True)
    await add_task(category_name="Дизайн", category_code="design",
                   subcategory_name="Иллюстрации", subcategory_code="illustration",
                   description="Нужно сделать логотип в стиле монограммы",
                   salary=10, status=True)
    await add_task(category_name="Дизайн", category_code="design",
                   subcategory_name="3Д-моделирование", subcategory_code="3d",
                   description="Нужно сделать логотип в стиле монограммы",
                   salary=10, status=True)

    await add_task(category_name="Маркетинг", category_code="marketing",
                   subcategory_name="Инстаграм", subcategory_code="inst",
                   description="Нужно сделать логотип в стиле монограммы",
                   salary=10, status=True)
    await add_task(category_name="Маркетинг", category_code="marketing",
                   subcategory_name="ВК", subcategory_code="vk", description="Нужно сделать логотип в стиле монограммы",
                   salary=10, status=True)
    await add_task(category_name="Маркетинг", category_code="marketing",
                   subcategory_name="Телеграм", subcategory_code="tg",
                   description="Нужно сделать логотип в стиле монограммы",
                   salary=10, status=True)
    await add_task(category_name="Маркетинг", category_code="marketing",
                   subcategory_name="Фейсбук", subcategory_code="fb",
                   description="Нужно сделать логотип в стиле монограммы",
                   salary=10, status=True)
    await add_task(category_name="Маркетинг", category_code="marketing",
                   subcategory_name="SEO-продвижение", subcategory_code="seo",
                   description="Нужно сделать логотип в стиле монограммы",
                   salary=10, status=True)

    await add_task(category_name="Копирайтинг", category_code="copywr",
                   subcategory_name="Статьи", subcategory_code="posts",
                   description="Нужно сделать логотип в стиле монограммы",
                   salary=10, status=True)
    await add_task(category_name="Копирайтинг", category_code="copywr",
                   subcategory_name="Переводы", subcategory_code="translate",
                   description="Нужно сделать логотип в стиле монограммы",
                   salary=10, status=True)
    await add_task(category_name="Копирайтинг", category_code="copywr",
                   subcategory_name="SEO-тексты", subcategory_code="seotxt",
                   description="Нужно сделать логотип в стиле монограммы",
                   salary=10, status=True)
    await add_task(category_name="Копирайтинг", category_code="copywr",
                   subcategory_name="Продающие тексты", subcategory_code="sellingtxt",
                   description="Нужно сделать логотип в стиле монограммы",
                   salary=10, status=True)

    await add_task(category_name="Разработка", category_code="dev",
                   subcategory_name="Front-end", subcategory_code="frontend",
                   description="Нужно сделать логотип в стиле монограммы",
                   salary=10, status=True)
    await add_task(category_name="Разработка", category_code="dev",
                   subcategory_name="Back-end", subcategory_code="backend",
                   description="Нужно сделать логотип в стиле монограммы",
                   salary=10, status=True)
    await add_task(category_name="Разработка", category_code="dev",
                   subcategory_name="Игры", subcategory_code="game",
                   description="Нужно сделать логотип в стиле монограммы",
                   salary=10, status=True)
    await add_task(category_name="Разработка", category_code="dev",
                   subcategory_name="Телеграм боты", subcategory_code="tgbots",
                   description="Нужно сделать логотип в стиле монограммы",
                   salary=10, status=True)
    await add_task(category_name="Разработка", category_code="dev",
                   subcategory_name="Лендинг", subcategory_code="landing",
                   description="Нужно сделать логотип в стиле монограммы",
                   salary=10, status=True)

    await add_task(category_name="Другое", category_code="other",
                   subcategory_name="Музыка", subcategory_code="music",
                   description="Нужно сделать логотип в стиле монограммы",
                   salary=10, status=True)
    await add_task(category_name="Другое", category_code="other",
                   subcategory_name="Видео", subcategory_code="video",
                   description="Нужно сделать логотип в стиле монограммы",
                   salary=10, status=True)
    await add_task(category_name="Другое", category_code="other",
                   subcategory_name="Фото", subcategory_code="photo",
                   description="Нужно сделать логотип в стиле монограммы",
                   salary=10, status=True)


async def add_freelancers():
    await add_freelancer(category_name="Дизайн", category_code="design",
                         subcategory_name="Веб-дизайн", subcategory_code="web",
                         bio="Я гений веба",github="#",
                         average_salary=5000, status=True)
    await add_freelancer(category_name="Дизайн", category_code="design",github="#",
                         subcategory_name="Анимации", subcategory_code="animation",
                         bio="Я гений анимации",
                         average_salary=5000, status=True)
    await add_freelancer(category_name="Дизайн", category_code="design",github="#",
                         subcategory_name="Логотипы", subcategory_code="logo",
                         bio="Я гений логотипов",
                         average_salary=5000, status=True)
    await add_freelancer(category_name="Дизайн", category_code="design",github="#",
                         subcategory_name="Иллюстрации", subcategory_code="illustration",
                         bio="Я гений иллюстрации",
                         average_salary=5000, status=True)
    await add_freelancer(category_name="Дизайн", category_code="design",github="#",
                         subcategory_name="3Д-моделирование", subcategory_code="3d",
                         bio="Я гени 3Д моделирования",
                         average_salary=5000, status=True)

    await add_freelancer(category_name="Маркетинг", category_code="marketing",github="#",
                         subcategory_name="Инстаграм", subcategory_code="inst",
                         bio="Я гений раскрутки в инстаграмме",
                         average_salary=5000, status=True)
    await add_freelancer(category_name="Маркетинг", category_code="marketing",github="#",
                         subcategory_name="ВК", subcategory_code="vk",
                         bio="Я гений в раскрутке ВК",
                         average_salary=5000, status=True)
    await add_freelancer(category_name="Маркетинг", category_code="marketing",github="#",
                         subcategory_name="Телеграм", subcategory_code="tg",
                         bio="Я гений раскрутки в Телеграмме",
                         average_salary=5000, status=True)
    await add_freelancer(category_name="Маркетинг", category_code="marketing",github="#",
                         subcategory_name="Фейсбук", subcategory_code="fb",
                         bio="Я гений раскрутки фейсбука",
                         average_salary=5000, status=True)
    await add_freelancer(category_name="Маркетинг", category_code="marketing",github="#",
                         subcategory_name="SEO-продвижение", subcategory_code="seo",
                         bio="Я гений SEO",
                         average_salary=5000, status=True)

    await add_freelancer(category_name="Копирайтинг", category_code="copywr",github="#",
                         subcategory_name="Статьи", subcategory_code="posts",
                         bio="Я гений статей",
                         average_salary=5000, status=True)
    await add_freelancer(category_name="Копирайтинг", category_code="copywr",github="#",
                         subcategory_name="Переводы", subcategory_code="translate",
                         bio="Я гений переводов",
                         average_salary=5000, status=True)
    await add_freelancer(category_name="Копирайтинг", category_code="copywr",github="#",
                         subcategory_name="SEO-тексты", subcategory_code="seotxt",
                         bio="Я гений SEO-текстов",
                         average_salary=5000, status=True)
    await add_freelancer(category_name="Копирайтинг", category_code="copywr",github="#",
                         subcategory_name="Продающие тексты", subcategory_code="sellingtxt",
                         bio="Я гений продающих текстов",
                         average_salary=5000, status=True)

    await add_freelancer(category_name="Разработка", category_code="dev",github="#",
                         subcategory_name="Front-end", subcategory_code="frontend",
                         bio="Я гений фронтенда",
                         average_salary=5000, status=True)
    await add_freelancer(category_name="Разработка", category_code="dev",github="#",
                         subcategory_name="Back-end", subcategory_code="backend",
                         bio="Я гений бекенда",
                         average_salary=5000, status=True)
    await add_freelancer(category_name="Разработка", category_code="dev",github="#",
                         subcategory_name="Игры", subcategory_code="game",
                         bio="Я гений игр",
                         average_salary=5000, status=True)
    await add_freelancer(category_name="Разработка", category_code="dev",github="#",
                         subcategory_name="Телеграм боты", subcategory_code="tgbots",
                         bio="Я гений телеграмм ботов",
                         average_salary=5000, status=True)
    await add_freelancer(category_name="Разработка", category_code="dev",github="#",
                         subcategory_name="Лендинг", subcategory_code="landing",
                         bio="Я гений лендингов",
                         average_salary=5000, status=True)

    await add_freelancer(category_name="Другое", category_code="other",github="#",
                         subcategory_name="Музыка", subcategory_code="music",
                         bio = "Я гений музыки",
                         average_salary=5000, status=True)
    await add_freelancer(category_name="Другое", category_code="other",github="#",
                         subcategory_name="Видео", subcategory_code="video",
                         bio="Я гений видео",
                         average_salary=5000, status=True)
    await add_freelancer(category_name="Другое", category_code="other",github="#",
                         subcategory_name="Фото", subcategory_code="photo",
                         bio="Я гений фотографии",
                         average_salary=5000, status=True)


loop = asyncio.get_event_loop()
loop.run_until_complete(create_db())
loop.run_until_complete(add_tasks())
loop.run_until_complete(add_freelancers())
