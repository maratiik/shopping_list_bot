from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from keyboards import *
from model import DataAccessObject, Base
import texts
from config_reader import DB_URL


router = Router()
dao = DataAccessObject(db_url=DB_URL, base=Base)


class BotState(StatesGroup):
    adding = State()
    main_menu = State()


@router.message(Command('start'))
async def cmd_start(message: Message, state: FSMContext):
    await state.set_state(BotState.main_menu)
    await message.answer(
        text=texts.MENU,
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

        if texts.HTTP in item:
            item_name = item[:item.find(texts.HTTP)]
            item_url = item[item.find(texts.HTTP):]
        else:
            item_name = item
        
        dao.save_item(item_name, item_url)


@router.callback_query(F.data == texts.ADD_CB)
async def btn_add(callback: CallbackQuery, state: FSMContext):
    await state.set_state(BotState.adding)
    await callback.message.edit_text(
        text=texts.ADD_TEXT,
        reply_markup=back_keyboard()
    )


@router.callback_query(F.data == texts.LIST_CB)
async def btn_list(callback: CallbackQuery):
    await callback.message.edit_text(
        text=texts.LIST_TEXT,
        reply_markup=keyboard_from_items(dao.get_all())
    )


@router.callback_query(F.data == texts.REMOVE_CB)
async def btn_remove(callback: CallbackQuery):
    await callback.message.edit_text(
        text=texts.REMOVE_TEXT,
        reply_markup=removing_keyboard_from_items(items=dao.get_all())
    )


@router.callback_query(F.data == texts.HELP_CB)
async def btn_help(callback: CallbackQuery):
    await callback.message.edit_text(
        text=texts.HELP_TEXT,
        reply_markup=back_keyboard()
    )


@router.callback_query(F.data == texts.BACK_CB)
async def btn_back(callback: CallbackQuery, state: FSMContext):
    await state.set_state(BotState.main_menu)
    await callback.message.edit_text(
        text=texts.MENU,
        reply_markup=menu_keyboard()
    )


@router.callback_query(F.data.startswith(texts.ITEM_CB))
async def btn_add_priority(callback: CallbackQuery):
    item_name = callback.data[len(texts.ITEM_CB):]
    dao.add_priority(item_name)
    await callback.message.edit_text(
        text=texts.LIST_TEXT,
        reply_markup=keyboard_from_items(dao.get_all())
    )


@router.callback_query(F.data.startswith(texts.NOTCHECKED_CB))
async def btn_check(callback: CallbackQuery):
    item_name = callback.data[len(texts.NOTCHECKED_CB):]
    dao.check_uncheck(item_name=item_name, set_to=1)
    await callback.message.edit_text(
        text=texts.REMOVE_TEXT,
        reply_markup=removing_keyboard_from_items(dao.get_all())
    )


@router.callback_query(F.data.startswith(texts.CHECKED_CB))
async def btn_uncheck(callback: CallbackQuery):
    item_name = callback.data[len(texts.CHECKED_CB):]
    dao.check_uncheck(item_name=item_name, set_to=0)
    await callback.message.edit_text(
        text=texts.REMOVE_TEXT,
        reply_markup=removing_keyboard_from_items(dao.get_all())
    )


@router.callback_query(F.data == texts.REMOVE_CHECKED_CB)
async def btn_remove_checked(callback: CallbackQuery):
    dao.remove_checked()
    await callback.message.edit_text(
        text=texts.LIST_TEXT,
        reply_markup=removing_keyboard_from_items(dao.get_all())
    )


@router.callback_query(F.data == texts.REMOVE_ALL_CB)
async def btn_remove_all(callback: CallbackQuery):
    dao.remove_all()
    await callback.message.edit_text(
        text=texts.LIST_TEXT,
        reply_markup=removing_keyboard_from_items(dao.get_all())
    )
