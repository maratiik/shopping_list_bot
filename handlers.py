from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
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
async def cmd_start(message: Message, state: FSMContext):
    await state.set_state(BotState.main_menu)
    await message.answer(
        text=MENU,
        reply_markup=menu_keyboard()
    )


@router.message(BotState.adding, F.text)
async def add_item(message: Message, state: FSMContext):
    # Добавляются айтемы каждого следующего
    # сообщения, пока юзер не нажмет BACK
    items_data = message.text.split(sep=', ')
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
async def btn_add(callback: CallbackQuery, state: FSMContext):
    await state.set_state(BotState.adding)
    await callback.message.edit_text(text=ADD_TEXT,
                                     reply_markup=back_keyboard())


@router.callback_query(F.data == LIST_CB)
async def btn_list(callback: CallbackQuery):
    await callback.message.edit_text(text=LIST_TEXT,
                                     reply_markup=keyboard_from_items(dao.get_all(),
                                                                      removing=False))


@router.callback_query(F.data == REMOVE_CB)
async def btn_remove(callback: CallbackQuery):
    await callback.message.edit_text(text=REMOVE_TEXT,
                                     reply_markup=keyboard_from_items(items=dao.get_all(),
                                                                      removing=True))


@router.callback_query(F.data == HELP_CB)
async def btn_help(callback: CallbackQuery):
    await callback.message.edit_text(text=HELP_TEXT,
                                     reply_markup=back_keyboard())


@router.callback_query(F.data == BACK_CB)
async def btn_back(callback: CallbackQuery, state: FSMContext):
    await state.set_state(BotState.main_menu)
    await callback.message.edit_text(text=MENU,
                                     reply_markup=menu_keyboard())


@router.callback_query(F.data.startswith(ITEM_CB))
async def btn_add_priority(callback: CallbackQuery):
    item_name = callback.data[len(ITEM_CB):]
    dao.add_priority(item_name)
    await callback.message.edit_text(text=LIST_TEXT,
                                     reply_markup=keyboard_from_items(dao.get_all(),
                                                                      removing=False))


@router.callback_query(F.data.startswith(NOTCHECKED_CB))
async def btn_check(callback: CallbackQuery):
    item_name = callback.data[len(NOTCHECKED_CB):]
    dao.check_uncheck(item_name=item_name, set_to=1)
    await callback.message.edit_text(text=REMOVE_TEXT,
                                     reply_markup=keyboard_from_items(dao.get_all(),
                                                                      removing=True))


@router.callback_query(F.data.startswith(CHECKED_CB))
async def btn_uncheck(callback: CallbackQuery):
    item_name = callback.data[len(CHECKED_CB):]
    dao.check_uncheck(item_name=item_name, set_to=0)
    await callback.message.edit_text(text=REMOVE_TEXT,
                                     reply_markup=keyboard_from_items(dao.get_all(),
                                                                      removing=True))


@router.callback_query(F.data == REMOVE_CHECKED_CB)
async def btn_remove_checked(callback: CallbackQuery):
    dao.remove_checked()
    await callback.message.edit_text(text=LIST_TEXT,
                                     reply_markup=keyboard_from_items(dao.get_all(),
                                                                      removing=True))


@router.callback_query(F.data == REMOVE_ALL_CB)
async def btn_remove_all(callback: CallbackQuery):
    dao.remove_all()
    await callback.message.edit_text(text=LIST_TEXT,
                                     reply_markup=keyboard_from_items(dao.get_all(),
                                                                      removing=True))