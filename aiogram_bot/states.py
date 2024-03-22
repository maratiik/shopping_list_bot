from aiogram.fsm.state import StatesGroup, State

class BotState(StatesGroup):
    menu = State()
    add = State()
    remove = State()