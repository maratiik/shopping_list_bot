from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.types import ReactionTypeEmoji
from aiogram.fsm.context import FSMContext

from sqlalchemy.orm import Session
from sqlalchemy import Engine

from texts import texts
from texts.text_makers import split_url
import keyboards.keyboards as keys
from util.states import BotState
from database.controller import ItemDAO, FavouriteDAO
from database.item_data import ItemData

import logging


logging.basicConfig(
    level=logging.DEBUG,
    filename='log.log',
    format='%(asctime)s %(levelname)s %(message)s'
)


fav_router = Router()


@fav_router.callback_query(F.data.startswith(texts.ITEM_CB), BotState._favourites)
async def btn_toggle_check_fav(callback: CallbackQuery, engine: Engine):
    item_name, item_url = split_url(callback.data[len(texts.ITEM_CB):])

    logging.debug(f"@fav_router.btn_toggle_check_fav: {item_name}, {item_url}")

    items = []

    with Session(engine) as session:
        dao = FavouriteDAO(session)
        dao.toggle_check(
            chat_id=callback.message.chat.id,
            item=ItemData(
                name=item_name,
                url=item_url
            )
        )

        items = dao.get_all(callback.message.chat.id)

    await callback.message.edit_reply_markup(
        reply_markup=keys.delete_keyboard(items)
    )


@fav_router.callback_query(F.data == texts.DELETE_CHECKED_CB, BotState._favourites)
async def btn_delete_checked_fav(callback: CallbackQuery, engine: Engine, state: FSMContext):
    await state.set_state(BotState._confirm_favs_checked)

    logging.debug(f"@fav_router.btn_delete_checked_fav")

    await callback.message.edit_text(
        text=texts.CONFIRM_DELETING_ALL_MENU_TEXT,
        reply_markup=keys.confirm_deleting_all()
    )


@fav_router.callback_query(F.data == texts.CONFIRM_DELETING_ALL_CB, BotState._confirm_favs_checked)
async def btn_confirm_delete_checked_fav(callback: CallbackQuery, engine: Engine, state: FSMContext):
    logging.debug('@fav_router.btn_confirm_delete_checked_fav')

    await state.set_state(BotState._favourites)

    with Session(engine) as session:
        dao = FavouriteDAO(session)
        dao.delete_checked(callback.message.chat.id)

        items = dao.get_all(callback.message.chat.id)

    await callback.message.edit_reply_markup(
        reply_markup=keys.delete_keyboard(items)
    )


@fav_router.callback_query(F.data == texts.DELETE_ALL_CB, BotState._favourites)
async def btn_delete_all_fav(callback: CallbackQuery, state: FSMContext, engine: Engine):

    logging.debug(f"@fav_router.btn_delete_all_fav")

    await state.set_state(BotState._confirm_favs)

    await callback.message.edit_text(
        text=texts.CONFIRM_DELETING_ALL_MENU_TEXT,
        reply_markup=keys.confirm_deleting_all()
    )


@fav_router.callback_query(F.data == texts.CONFIRM_DELETING_ALL_CB, BotState._confirm_favs)
async def btn_confirm_delete_all_fav(callback: CallbackQuery, engine: Engine, state: FSMContext):
    logging.debug("@fav_router.btn_confirm_delete_all_fav")

    await state.set_state(BotState._main_menu)
    
    with Session(engine) as session:
        dao = FavouriteDAO(session)
        dao.delete_all(callback.message.chat.id)

    await callback.message.edit_text(
        text=texts.MENU_TEXT,
        reply_markup=keys.menu_keyboard()
    )


@fav_router.callback_query(F.data == texts.BACK_CB, BotState._favourites)
async def btn_back_fav(callback: CallbackQuery, state: FSMContext):

    logging.debug(f"@fav_router.btn_back_fav")

    await state.set_state(BotState._main_menu)

    await callback.message.edit_text(
        text=texts.MENU_TEXT,
        reply_markup=keys.menu_keyboard()
    )


@fav_router.callback_query(F.data == texts.BACK_CB, BotState._confirm_favs)
async def btn_cancel_delete_all_fav(callback: CallbackQuery, state: FSMContext, engine: Engine):
    logging.debug("@fav_router.btn_cancel_delete_all_fav")

    await state.set_state(BotState._favourites)

    with Session(engine) as session:
        dao = FavouriteDAO(session)
        items = dao.get_all(callback.message.chat.id)

    await callback.message.edit_text(
        text=texts.FAVOURITES_MENU_TEXT,
        reply_markup=keys.delete_keyboard(items)
    )


@fav_router.callback_query(F.data == texts.BACK_CB, BotState._confirm_favs_checked)
async def btn_cancel_delete_checked_fav(callback: CallbackQuery, state: FSMContext, engine: Engine):
    logging.debug('@fav_router.btn_cancel_delete_checked_fav')

    await state.set_state(BotState._favourites)

    with Session(engine) as session:
        dao = FavouriteDAO(session)
        items = dao.get_all(callback.message.chat.id)

    await callback.message.edit_text(
        text=texts.FAVOURITES_MENU_TEXT,
        reply_markup=keys.delete_keyboard(items)
    )
    