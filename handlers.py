from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery, ReactionTypeEmoji
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from keyboards import *
import texts
from config_reader import DB_URL
from dao import ItemDAO
from model import Item, Base

import random


router = Router()
engine = create_engine(DB_URL)
Base.metadata.create_all(engine)


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
        
        with Session(engine) as session:
            dao = ItemDAO(session)
            dao.save(item_name, item_url)
            
    emoji = random.choice(texts.EMOJIS)
    await message.react([ReactionTypeEmoji(emoji=emoji)])
        

@router.callback_query(F.data == texts.ADD_CB)
async def btn_add(callback: CallbackQuery, state: FSMContext):
    await state.set_state(BotState.adding)
    await callback.message.edit_text(
        text=texts.ADD_TEXT,
        reply_markup=back_keyboard()
    )


@router.callback_query(F.data == texts.LIST_CB)
async def btn_list(callback: CallbackQuery):
    with Session(engine) as session:
        dao = ItemDAO(session)
        items = dao.get_all()

    await callback.message.edit_text(
        text=texts.LIST_TEXT,
        reply_markup=keyboard_from_items(items)
    )


@router.callback_query(F.data == texts.REMOVE_CB)
async def btn_remove(callback: CallbackQuery):
    with Session(engine) as session:
        dao = ItemDAO(session)
        items = dao.get_all()

    await callback.message.edit_text(
        text=texts.REMOVE_TEXT,
        reply_markup=removing_keyboard_from_items(items)
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
    items = []

    with Session(engine) as session:
        dao = ItemDAO(session)
        dao.add_priority(item_name)
        items = dao.get_all()

    await callback.message.edit_text(
        text=texts.LIST_TEXT,
        reply_markup=keyboard_from_items(items)
    )


@router.callback_query(F.data.startswith(texts.NOTCHECKED_CB))
async def btn_check(callback: CallbackQuery):
    item_name = callback.data[len(texts.NOTCHECKED_CB):]
    items = []

    with Session(engine) as session:
        dao = ItemDAO(session)
        dao.check_uncheck(item_name=item_name, set_to=True)
        items = dao.get_all()


    await callback.message.edit_text(
        text=texts.REMOVE_TEXT,
        reply_markup=removing_keyboard_from_items(items)
    )


@router.callback_query(F.data.startswith(texts.CHECKED_CB))
async def btn_uncheck(callback: CallbackQuery):
    item_name = callback.data[len(texts.CHECKED_CB):]
    items = []

    with Session(engine) as session:
        dao = ItemDAO(session)
        dao.check_uncheck(item_name=item_name, set_to=False)
        items = dao.get_all()

    await callback.message.edit_text(
        text=texts.REMOVE_TEXT,
        reply_markup=removing_keyboard_from_items(items)
    )


@router.callback_query(F.data == texts.REMOVE_CHECKED_CB)
async def btn_remove_checked(callback: CallbackQuery):
    items = []

    with Session(engine) as session:
        dao = ItemDAO(session)
        dao.delete_checked()
        items = dao.get_all()

    await callback.message.edit_text(
        text=texts.LIST_TEXT,
        reply_markup=removing_keyboard_from_items(items)
    )


@router.callback_query(F.data == texts.REMOVE_ALL_CB)
async def btn_remove_all(callback: CallbackQuery):
    with Session(engine) as session:
        dao = ItemDAO(session)
        dao.delete_all()

    await callback.message.edit_text(
        text=texts.MENU,
        reply_markup=menu_keyboard()
    )
