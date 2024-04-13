from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.types import ReactionTypeEmoji
from aiogram.fsm.context import FSMContext

from sqlalchemy.orm import Session
from sqlalchemy import Engine

from texts import texts
import texts.text_makers as tm
import keyboards.keyboards as keys
from util.states import BotState
from database.controller import ItemDAO, FavouriteDAO
from database.item_data import ItemData

from random import choice

import logging


logging.basicConfig(
    level=logging.DEBUG,
    filename='log.log',
    format='%(asctime)s %(levelname)s %(message)s'
)


adding_router = Router()


@adding_router.message(F.text, BotState._adding)
async def add_item(message: Message, state: FSMContext, bot: Bot, engine: Engine):
    items_data = message.text.split(sep=', ')

    logging.debug(f"@adding_router.add_item: {items_data}")

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
            dao.save(
                chat_id=message.chat.id,
                item=ItemData(
                    name=item_name,
                    url=item_url
                )
            )

    chat = await bot.get_chat(chat_id=message.chat.id)
    emojis = chat.available_reactions

    logging.debug(f"CHECKING AVAILABLE REACTIONS: {emojis}")

    if emojis != None:
        if len(emojis):
            response_emoji = choice(emojis).emoji
            await message.react([ReactionTypeEmoji(emoji=response_emoji)])
    else:
        await message.react([ReactionTypeEmoji(emoji=choice(texts.EMOJIS))])


@adding_router.callback_query(F.data.startswith(texts.ITEM_CB), BotState._adding)
async def btn_add_from_fav(callback: CallbackQuery, engine: Engine):
    item_data = callback.data[len(texts.ITEM_CB):]

    logging.debug(f"@adding_router.btn_add_from_fav: {item_data}")

    item_name, item_url = tm.split_url(item_data)

    with Session(engine) as session:
        dao = ItemDAO(session)
        dao.save(
            chat_id=callback.message.chat.id,
            item=ItemData(
                name=item_name,
                url=item_url
            )
        )
    
    await callback.answer(text=f'{item_name} добавлен!')


@adding_router.callback_query(F.data == texts.BACK_CB, BotState._adding)
async def btn_back_from_adding(callback: CallbackQuery, state: FSMContext):
    logging.debug('@adding_router.btn_back_from_adding')
    
    await state.set_state(BotState._main_menu)

    await callback.message.edit_text(
        text=texts.MENU_TEXT,
        reply_markup=keys.menu_keyboard()
    )
    