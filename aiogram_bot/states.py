from aiogram.fsm.state import StatesGroup, State

class BotState(StatesGroup):
    _menu = State()
    _add = State()
    _list = State()
    _remove = State()