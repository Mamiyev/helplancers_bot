from aiogram.dispatcher.filters.state import StatesGroup, State


class Profile(StatesGroup):
    about = State()
    hourly_rate = State()
    github = State()


class Freelancer(StatesGroup):
    freelancer = State()
    finality = State()