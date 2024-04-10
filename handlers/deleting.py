from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.types import ReactionTypeEmoji
from aiogram.fsm.context import FSMContext

from sqlalchemy.orm import Session
from sqlalchemy import Engine

from texts import texts
from text.text_makers import split_url
import keyboards.keyboards as keys
from util.states import BotState
from database.controller import ItemDAO, FavouriteDAO
from database.item_data import ItemData


delete_router = Router()


@delete_router.callback_query(F.data.startswith(texts.ITEM_CB), BotState._deleting)
async def btn_toggle_check(callback: CallbackQuery, engine: Engine):
    item_name, item_url = split_url(callback.data[len(texts.ITEM_CB):])

    items = []

    with Session(engine) as session:
        dao = ItemDAO(session)
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


@delete_router.callback_query(F.data == texts.DELETE_CHECKED_CB, BotState._deleting)
async def btn_delete_checked(callback: CallbackQuery, engine: Engine):
    items = []

    with Session(engine) as session:
        dao = ItemDAO(session)
        dao.delete_checked(callback.message.chat.id)
        items = dao.get_all(callback.message.chat.id)

    await callback.message.edit_reply_markup(
        reply_markup=keys.delete_keyboard(items)
    )


@delete_router.callback_query(F.data == texts.DELETE_ALL_CB, BotState._deleting)
async def btn_delete_all(callback: CallbackQuery, state: FSMContext, engine: Engine):
    await state.set_state(BotState._main_menu)

    with Session(engine) as session:
        dao = ItemDAO(session)
        dao.delete_all(callback.message.chat.id)

    await callback.message.edit_text(
        text=texts.MENU_TEXT,
        reply_markup=keys.menu_keyboard()
    )
