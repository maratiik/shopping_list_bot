from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.types import Message

from sqlalchemy import create_engine

from ..database.model import Base
from ..util.states import BotState
from ..texts.texts import MENU_TEXT
from ..keyboards.keyboards import menu_keyboard


start_router = Router()


@start_router.message(Command('start'))
async def cmd_start(message: Message, state: FSMContext):
    await state.set_state(BotState._main_menu)
    await message.answer(
        text=MENU_TEXT,
        reply_markup=menu_keyboard()
    )
