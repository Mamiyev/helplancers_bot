from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from utils.db_api.db_commands import get_categories, count_freelancers, get_subcategories

menu_cd = CallbackData("show_menu", "level", "category", "subcategory")


def make_callback_data(level, category="0", subcategory="0"):
    return menu_cd.new(level=level, category=category, subcategory=subcategory)


async def categories_keyboard():
    CURRENT_LEVEL = 0
    markup = InlineKeyboardMarkup(row_width=1)

    categories = await get_categories()
    for category in categories:
        if category.category_code == '0' or category.category_code == 'Null' or not category.category_code:
            continue
        button_text = f"{category.category_name}"
        callback_data = make_callback_data(level=CURRENT_LEVEL + 1, category=category.category_code)

        markup.insert(
            InlineKeyboardButton(text=button_text, callback_data=callback_data)
        )
    return markup


async def subcategories_keyboard(category):
    CURRENT_LEVEL = 1
    markup = InlineKeyboardMarkup(row_width=1)

    subcategories = await get_subcategories(category_code=category)
    for subcategory in subcategories:
        if subcategory.subcategory_code == '0':
            continue
        button_text = f"{subcategory.subcategory_name}"
        callback_data = make_callback_data(level=CURRENT_LEVEL + 1, category=category,
                                           subcategory=subcategory.subcategory_code)

        markup.insert(
            InlineKeyboardButton(text=button_text, callback_data=callback_data)
        )
    markup.row(
        InlineKeyboardButton(
            text="Назад",
            callback_data=make_callback_data(level=CURRENT_LEVEL - 1, category=category)
        )
    )
    return markup


async def last_keyboard(category, subcategory):
    CURRENT_LEVEL = 2
    markup = InlineKeyboardMarkup(row_width=2)
    markup.insert(
        InlineKeyboardButton(
            text="Назад",
            callback_data=make_callback_data(level=CURRENT_LEVEL - 1, category=category, subcategory=subcategory)
        )
    )
    markup.insert(
        InlineKeyboardButton(
            text="Подтвердить",
            callback_data=make_callback_data(level=CURRENT_LEVEL + 1, category=category, subcategory=subcategory)
        )
    )
