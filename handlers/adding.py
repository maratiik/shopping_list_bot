from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.types import ReactionTypeEmoji
from aiogram.fsm.context import FSMContext

from sqlalchemy.orm import Session
from sqlalchemy import Engine

from texts import texts
import keyboards.keyboards as keys
from util.states import BotState
from database.controller import ItemDAO, FavouriteDAO
from database.item_data import ItemData

from random import choice


adding_router = Router()


@adding_router.message(BotState._adding, F.text)
async def add_item(message: Message, state: FSMContext, bot: Bot, engine: Engine):
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
            dao.save(
                chat_id=message.chat.id,
                item=ItemData(
                    name=item_name,
                    url=item_url
                )
            )

    chat = await bot.get_chat(chat_id=message.chat.id)
    emojis = chat.available_reactions

    if emojis != None:
        if len(emojis):
            response_emoji = choice(emojis)
            await message.react([ReactionTypeEmoji(emoji=response_emoji)])
    else:
        await message.react([ReactionTypeEmoji(emoji=choice(texts.EMOJIS))])


@adding_router.callback_query(BotState._adding, F.data.startswith(texts.ITEM_CB))
async def btn_add_from_fav(callback: CallbackQuery, engine: Engine):
    item_data = callback.data[len(texts.ITEM_CB)]

    item_name = ''
    item_url = ''

    if texts.HTTP in item_data:
        item_name = item_data[:item_data.find(texts.HTTP)]
        item_url = item_data[item_data.find(texts.HTTP):]
    else:
        item_name = item_data

    with Session(engine) as session:
        dao = ItemDAO(session)
        dao.save(
            chat_id=message.chat.id,
            item=ItemData(
                name=item_name,
                url=item_url
            )
        )
    
    await callback.answer(text=f'{item_name} добавлен!')