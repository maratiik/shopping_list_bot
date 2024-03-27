from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from keyboards import *
from model import DataAccessObject
from texts import *
from config_reader import DB_URL


router = Router()
dao = DataAccessObject(db_url=DB_URL)


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
    # Добавляются айтемы каждого следующего
    # сообщения, пока юзер не нажмет BACK
    items_data = message.split(', ')
    for item in items_data:
        item_name = ''
        item_url = ''

        if HTTP in item:
            item_name = item[:item.find(HTTP)]
            item_url = item[item.find(HTTP):]
        else:
            item_name = item
        
        dao.save_item(item_name, item_url)


@router.callback_query(F.data == ADD_CB)
async def btn_add(message: Message, state: FSMContext):
    await state.set_state(BotState.adding)
    await message.edit_text(text=ADD_TEXT,
                            reply_markup=back_keyboard())


@router.callback_query(F.data == LIST_CB)
async def btn_list(message: Message):
    await message.edit_text(text=LIST_TEXT,
                            reply_markup=keyboard_from_items(dao.get_all()))


@router.callback_query(F.data == REMOVE_CB)
async def btn_remove(message: Message):
    await message.edit_text(text=REMOVE_TEXT,
                            reply_markup=keyboard_from_items(items=dao.get_all(),
                                                             removing=True))


@router.callback_query(F.data == HELP)
async def btn_help(message: Message):
    await message.edit_text(text=HELP_TEXT,
                            reply_markup=back_keyboard())