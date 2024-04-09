from aiogram.fsm.state import State, StatesGroup


class BotState(StatesGroup):

    _main_menu = State()
    _adding = State()
    _favourites = State()
    _deleting = State()
    _list = State()
    _detail = State()
    _help = State()
