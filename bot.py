from config_reader import *

import asyncio
from aiogram import Bot, Dispatcher


async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    #TODO: make handlers
    # dp.include_routers(...)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
