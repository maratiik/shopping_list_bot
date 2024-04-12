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

list_router = Router()


@list_router.callback_query(BotState._list, F.data.startswith(texts.ITEM_CB))
async def btn_item_detail(callback: CallbackQuery, state: FSMContext, engine: Engine, data: dict):
    await state.set_state(BotState._detail)

    logging.debug(f"@list_router.btn_item_detail: {callback.data}")

    data['item_name'], data['item_url'] = split_url(callback.data[len(texts.ITEM_CB):])

    await callback.message.edit_reply_markup(
        reply_markup=keys.item_detail_keyboard(
            detailed_item=data['item_name'],
            items=data['items']
        )
    )


@list_router.callback_query(BotState._detail, F.data.startswith(texts.ITEM_CB))
async def btn_item_general(callback: CallbackQuery, state: FSMContext, engine: Engine, data: dict):

    logging.debug(f"@list_router.btn_item_general")

    await state.set_state(BotState._list)

    data['item_name'] = ''
    data['item_url'] = ''
    # items = []

    # with Session(engine) as session:
    #     dao = ItemDAO(session)
    #     items = dao.get_all_with_fav_data(callback.message.chat.id)

    await callback.message.edit_reply_markup(
        reply_markup=keys.list_keyboard(data['items'])
    )


@list_router.callback_query(BotState._detail, F.data == texts.ADD_PRIRORITY_CB)
async def btn_add_priority(callback: CallbackQuery, state: FSMContext, engine: Engine, data: dict):
    item_name = data['item_name']

    logging.debug(f"@list_router.btn_add_priority: {item_name}")

    with Session(engine) as session:
        dao = ItemDAO(session)
        dao.add_priority(
            chat_id=callback.message.chat.id,
            item=ItemData(name=item_name)
        )

        data['items'] = dao.update_data(
            chat_id=callback.message.chat.id,
            items=data['items']
        )

    await callback.message.edit_reply_markup(
        reply_markup=keys.item_detail_keyboard(
            detailed_item=item_name,
            items=data['items']
        )
    )


@list_router.callback_query(BotState._detail, F.data == texts.ADD_TO_FAV_CB)
async def btn_add_to_fav(callback: CallbackQuery, state: FSMContext, engine: Engine, data: dict):
    item_name = data['item_name']
    item_url = data['item_url']

    logging.debug(f"@list_router.btn_add_to_fav: {item_name}")

    item_data: ItemData = None

    with Session(engine) as session:
        fav_dao = FavouriteDAO(session)

        if fav_dao.exists(
            chat_id=callback.message.chat.id,
            item=ItemData(
                name=item_name,
                url=item_url
            )
        ):
            fav_dao.delete_one(
                chat_id=callback.message.chat.id,
                item=ItemData(name=item_name)
            )

            item_data = ItemData(
                name=item_name,
                url=item_url,
                is_fav=False
            )
        else:
            fav_dao.save(
                chat_id=callback.message.chat.id,
                item=ItemData(
                    name=item_name,
                    url=item_url
                )
            )

            item_data = ItemData(
                name=item_name,
                url=item_url,
                is_fav=True
            )
        
        item_dao = ItemDAO(session)
        data['items'] = item_dao.update_data(
            chat_id=callback.message.chat.id,
            items=data['items']
        )

    await callback.message.edit_reply_markup(
        reply_markup=keys.item_detail_keyboard(
            detailed_item=item_name,
            items=data['items']
        )
    )


@list_router.callback_query(BotState._detail, F.data == texts.CHECK_CB)
async def btn_toggle_check(callback: CallbackQuery, engine: Engine, data: dict):
    item_name = data['item_name']
    item_url = data['item_url']

    logging.debug(f"@list_router.btn_toggle_check: {item_name}")

    with Session(engine) as session:
        dao = ItemDAO(session)
        dao.toggle_check(
            chat_id=callback.message.chat.id,
            item=ItemData(
                name=item_name,
                url=item_url
            )
        )

        data['items'] = dao.update_data(
            chat_id=callback.message.chat.id,
            items=data['items']
        )

    await callback.message.edit_reply_markup(
        reply_markup=keys.item_detail_keyboard(
            detailed_item=item_name,
            items=data['items']
        )
    )


@list_router.callback_query(BotState._list, F.data == texts.DELETE_CHECKED_CB)
async def btn_delete_checked(callback: CallbackQuery, engine: Engine, data: dict, state: FSMContext):

    logging.debug(f"@list_router.btn_delete_checked")

    await state.set_state(BotState._confirm_list_checked)

    await callback.message.edit_text(
        text=texts.CONFIRM_DELETING_ALL_MENU_TEXT,
        reply_markup=keys.confirm_deleting_all()
    )


@list_router.callback_query(BotState._confirm_list_checked, F.data == texts.CONFIRM_DELETING_ALL_CB)
async def btn_confirm_delete_checked(callback: CallbackQuery, engine: Engine, data: dict, state: FSMContext):
    logging.debug('@list_router.btn_confirm_delete_checked')

    await state.set_state(BotState._list)

    data['items'] = []

    with Session(engine) as session:
        dao = ItemDAO(session)
        dao.delete_checked(callback.message.chat.id)
        items = dao.get_all(callback.message.chat.id)

    await callback.message.edit_reply_markup(
        reply_markup=keys.list_keyboard(items)
    )


@list_router.callback_query(BotState._list, F.data == texts.DELETE_ALL_CB)
async def btn_delete_all(callback: CallbackQuery, engine: Engine, data: dict, state: FSMContext):
    logging.debug(f"@list_router.btn_delete_all")

    await state.set_state(BotState._confirm_list)

    await callback.message.edit_text(
        text=texts.CONFIRM_DELETING_ALL_MENU_TEXT,
        reply_markup=keys.confirm_deleting_all()
    )
    


@list_router.callback_query(BotState._confirm_list, F.data == texts.CONFIRM_DELETING_ALL_CB)
async def btn_confirm_delete_all(callback: CallbackQuery, engine: Engine, data: dict, state: FSMContext):
    logging.debug(f"@list_router.btn_confirm_delete_all")

    await state.set_state(BotState._main_menu)

    data['items'] = []

    with Session(engine) as session:
        dao = ItemDAO(session)
        dao.delete_all(callback.message.chat.id)

    await callback.message.edit_text(
        text=texts.MENU_TEXT,
        reply_markup=keys.menu_keyboard()
    )


@list_router.callback_query(BotState._confirm_list, F.data == texts.BACK_CB)
async def btn_cancel_delete_all(callback: CallbackQuery, state: FSMContext, data: dict):
    logging.debug("@list_router.btn_cancel_delete_all")

    await state.set_state(BotState._list)

    await callback.message.edit_text(
        text=texts.LIST_MENU_TEXT,
        reply_markup=keys.list_keyboard(data['items'])
    )


@list_router.callback_query(BotState._list, F.data == texts.BACK_CB)
async def btn_back_from_list(callback: CallbackQuery, state: FSMContext, data: dict):
    logging.debug('@list_router.btn_back_from_list')

    await state.set_state(BotState._main_menu)

    data['items'] = []

    await callback.message.edit_text(
        text=texts.MENU_TEXT,
        reply_markup=keys.menu_keyboard()
    )
    

@list_router.callback_query(BotState._confirm_list_checked, F.data == texts.BACK_CB)
async def btn_cancel_delete_checked(callback: CallbackQuery, state: FSMContext, data: dict):
    logging.debug('@list_router.btn_cancel_delete_checked')

    await state.set_state(BotState._list)

    await callback.message.edit_text(
        text=texts.LIST_MENU_TEXT,
        reply_markup=keys.list_keyboard(data['items'])
    )
