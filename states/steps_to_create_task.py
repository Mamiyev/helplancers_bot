from aiogram.dispatcher.filters.state import StatesGroup, State

class Task_state(StatesGroup):
    start = State()
    category = State()
    subcategory = State()
    description = State()
    salary = State()
    pre_finished = State()
    finished = State()
    mailing = State()
