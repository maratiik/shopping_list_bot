import config_reader as conf
from model import DataAccessObject, Base
from handlers import router
from middleware import SessionMiddleware

import asyncio
from aiogram import Bot, Dispatcher

from sqlalchemy import create_engine
from sqlalchemy.orm import Session


async def main():
    bot = Bot(token=conf.TOKEN)
    dp = Dispatcher()
    
    engine = create_engine(conf.DB_URL)
    Base.metadata.create_all(engine)

    dp.include_router(router)
    dp.message.outer_middleware(SessionMiddleware(engine))

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())