from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from keyboards import *
from texts import MENU, HTTP


router = Router()


class BotState(StatesGroup):
    adding = State()
    main_menu = State()


@router.message(Command('start'))
async def cmd_start(message: Message):
    await message.answer(
        text=MENU,
        reply_markup=menu_keyboard()
    )


@router.message(BotState.adding, F.text)
async def add_item(message: Message, state: FSMContext):
    pass

def ht(s: str):
    if HTTP in s:
        a = s.split(HTTP, 2)
        first = a[0]
        second = a[1]
        print(first)
        print(second)
    else:
        print(s)


if __name__ == '__main__':
    s = 'github https://github.com/MasterGroosha/aiogram-3-guide/blob/master/code/07_fsm/handlers/ordering_food.py'
    ht(s)