import asyncio
import logging
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from util.config_reader import TOKEN, DB_URL
from database.model import Base
from handlers.start import start_router
from handlers.main_menu import menu_router
from handlers.adding import adding_router
from handlers.list import list_router
from handlers.deleting import delete_router
from handlers.favourites import fav_router

from aiogram import Bot, Dispatcher

from sqlalchemy import create_engine

engine = create_engine(DB_URL)
Base.metadata.create_all(engine)

logging.basicConfig(
    level=logging.DEBUG,
    filename='log.log',
    format='%(asctime)s %(levelname)s %(message)s'
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    dp['bot'] = bot
    dp['engine'] = engine
    dp['data'] = {'item_name': '', 'item_url': ''}

    dp.include_routers(
        start_router,
        menu_router,
        adding_router,
        list_router,
        delete_router,
        fav_router
    )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except Exception as e:
        logging.exception(e)
