from aiogram.fsm.state import State, StatesGroup


class BotState(StatesGroup):

    _main_menu = State()
    _adding = State()
    _favourites = State()
    _deleting = State()
    _list = State()
    _detail = State()
    _help = State()

    _confirm_list = State()
    _confirm_favs = State()

    _confirm_list_checked = State()
    _confirm_favs_checked = State()
