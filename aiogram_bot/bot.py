import ascyncio
import os

from config_reader import TOKEN

from keyboards import *
from ..settings import *
from Model.item import *
from states import BotState

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext

bot = Bot(token=TOKEN)
dp = Dispatcher()


async def main():
    await dp.start_polling(bot)


@dp.message(Command('start'))
async def cmd_start(message: types.Message):
    await message.answer('Меню',
                        reply_markup=menu_keyboard())


@dp.message(F.text)
async def cmd_add(message: types.Message, state: FSMContext):
    items = message.text.split(sep=', ')

    for item in items:
        item_url = ''
        if HTTP in item:
            item_name = item[:item.find(HTTP) - 1]
            item_url = item[item.find(HTTP):]
        else:
            item_name = item

        add(item_name, item_url)

    await state.set_state(BotState._menu)
    await bot.edit_message_reply_markup(reply_markup=menu_keyboard())
    await message.answer('Добавлено!')


@dp.callback_query_handler(func=lambda c: c.data == ADD)
async def process_btn_add(callback_query: types.CallbackQuery, state: FSMContext):
    await state.set_state(BotState._add)
    await bot.edit_message_reply_markup(reply_markup=help_add_keyboard())


@dp.callback_query_handler(func=lambda c: c.data == LIST)
async def process_btn_list(callback_query: types.CallbackQuery, state: FSMContext):
    


if __name__ == '__main__':
    ascyncio.run(main())