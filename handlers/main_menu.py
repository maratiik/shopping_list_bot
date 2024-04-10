from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from sqlalchemy.orm import Session
from sqlalchemy import Engine

from texts import texts
import keyboards.keyboards as keys
from util.states import BotState
from database.controller import ItemDAO, FavouriteDAO

import logging


logging.basicConfig(
    level=logging.DEBUG,
    filename='log.log',
    format='%(asctime)s %(levelname)s %(message)s'
)

menu_router = Router()


@menu_router.callback_query(F.data == texts.ADD_CB, BotState._main_menu)
async def btn_add(callback: CallbackQuery, state: FSMContext, engine: Engine):

    logging.debug(f"@menu_router.btn_add")

    await state.set_state(BotState._adding)

    items = []

    with Session(engine) as session:
        dao = FavouriteDAO(session)
        items = dao.get_all(callback.message.chat.id)

    await callback.message.edit_text(
        text=texts.ADD_MENU_TEXT,
        reply_markup=keys.adding_keyboard(items)
    )


@menu_router.callback_query(F.data == texts.LIST_CB, BotState._main_menu)
async def btn_list(callback: CallbackQuery, state: FSMContext, engine: Engine):

    logging.debug(f"@menu_router.btn_list")

    await state.set_state(BotState._list)

    items = []

    with Session(engine) as session:
        dao = ItemDAO(session)
        items = dao.get_all_with_fav_data(callback.message.chat.id)

    await callback.message.edit_text(
        text=texts.LIST_MENU_TEXT,
        reply_markup=keys.list_keyboard(items)
    )


@menu_router.callback_query(F.data == texts.DELETE_CB, BotState._main_menu)
async def btn_delete(callback: CallbackQuery, state: FSMContext, engine: Engine):

    logging.debug(f"@menu_router.btn_delete")

    await state.set_state(BotState._deleting)

    items = []

    with Session(engine) as session:
        dao = ItemDAO(session)
        items = dao.get_all(callback.message.chat.id)

    await callback.message.edit_text(
        text=texts.DELETE_MENU_TEXT,
        reply_markup=keys.delete_keyboard(items)
    )


@menu_router.callback_query(F.data == texts.FAVOURITES_CB, BotState._main_menu)
async def btn_favourites(callback: CallbackQuery, state: FSMContext, engine: Engine):

    logging.debug(f"@menu_router.btn_favourites")

    await state.set_state(BotState._favourites)

    items = []

    with Session(engine) as session:
        dao = FavouriteDAO(session)
        items = dao.get_all(callback.message.chat.id)

    await callback.message.edit_text(
        text=texts.FAVOURITES_MENU_TEXT,
        reply_markup=keys.delete_keyboard(items)
    )


@menu_router.callback_query(F.data == texts.HELP_CB)
async def btn_help(callback: CallbackQuery, state: FSMContext):

    logging.debug(f"@menu_router.btn_help")

    await state.set_state(BotState._help)

    await callback.message.edit_text(
        text=texts.HELP_MENU_TEXT,
        reply_markup=keys.back_keyboard()
    )


@menu_router.callback_query(F.data == texts.BACK_CB)
async def btn_back(callback: CallbackQuery, state: FSMContext):

    logging.debug(f"@menu_router.btn_back")
    
    await state.set_state(BotState._main_menu)

    await callback.message.edit_text(
        text=texts.MENU_TEXT,
        reply_markup=keys.menu_keyboard()
    )
