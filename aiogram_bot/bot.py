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


@dp.message(F.text, BotState._add)
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
    await bot.edit_message_reply_markup(chat_id=callback_query.message.chat.id,
                                        message_id=callback_query.message.message_id,
                                        reply_markup=back_keyboard())


@dp.callback_query_handler(func=lambda c: c.data == LIST)
async def process_btn_list(callback_query: types.CallbackQuery, state: FSMContext):
    await state.set_state(BotState._list)

    count = get_count()

    if count == 0:
        await bot.answer_callback_query(callback_query.id, 'Список пуст!')
    else:
        await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                              message_id=callback_query.message.message_id,
                              reply_markup=list_keyboard())


@dp.callback_query_handler(func=lambda c: c.data == BACK)
async def process_btn_back(callback_query: types.CallbackQuery, state: FSMContext):
    await state.set_state(BotState._menu)
    await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                message_id=callback_query.message.message_id,
                                text='Меню',
                                reply_markup=menu_keyboard())


@dp.callback_query_handler(func=lambda c: c.data == REMOVE)
async def process_btn_remove(callback_query: types.CallbackQuery, state: FSMContext):
    await state.set_state(BotState._remove)

    count = get_count()

    if count == 0:
        await bot.answer_callback_query(callback_query_id=callback_query.id,
                                        text='Нечего удалять!')
    else:
        await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                    message_id=callback_query.message.message_id,
                                    text='Удаляем-с',
                                    reply_markup=remove_keyboard())


@dp.callback_query_handler(func=lambda c: c.data.startswith(CHECKED), BotState._remove)
async def process_item_uncheck(callback_query: types.CallbackQuery, state: FSMContext):
    item_name = callback_query.data.split('_', 1)[1]
    check_uncheck(item_name, 0)
    
    await bot.edit_message_reply_markup(chat_id=callback_query.message.chat.id,
                                        message_id=callback_query.message.message_id,
                                        reply_markup=remove_keyboard())


@dp.callback_query_handler(func=lambda c: c.data.startswith(NOT_CHECKED), BotState._remove)
async def process_item_check(callback_query: types.CallbackQuery, state: FSMContext):
    item_name = callback_query.data.split('_', 1)[1]
    check_uncheck(item_name, 1)

    await bot.edit_message_reply_markup(chat_id=callback_query.message.chat.id,
                                        message_id=callback_query.message.message_id,
                                        reply_markup=remove_keyboard())


@dp.callback_query_handler(func=lambda c: c.data == REMOVE_CHECKED)
async def process_btn_remove_checked(callback_query: types.CallbackQuery, state: FSMContext):
    remove_checked()

    count = get_count()

    if count == 0:
        await bot.answer_callback_query(callback_query_id=callback_query.id,
                                        text='Список очищен!')
        await state.set_state(BotState._menu)
        await bot.edit_message_reply_markup(chat_id=callback_query.message.chat.id,
                                            message_id=callback_query.message.message_id,
                                            reply_markup=menu_keyboard())
    else:
        await bot.edit_message_reply_markup(chat_id=callback_query.message.chat.id,
                                            message_id=callback_query.message.message_id,
                                            reply_markup=remove_keyboard())


@dp.callback_query_handler(func=lambda c: c.data == REMOVE_ALL)
async def process_btn_remove_all(callback_query: types.CallbackQuery, state: FSMContext):
    remove_all()
    
    await bot.answer_callback_query(callback_query_id=callback_query.id,
                                    text='Список очищен!')
    await state.set_state(BotState._menu)
    await bot.edit_message_reply_markup(chat_id=callback_query.message.chat.id,
                                        message_id=callback_query.message.message_id,
                                        reply_markup=menu_keyboard())


@dp.callback_query_handler(func=lambda c: c.data == HELP):
async def process_btn_help(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                message_id=callback_query.message.message_id,
                                text=HELP_MESSAGE,
                                reply_markup=back_keyboard())


@dp.callback_query_handler(func=lambda c: )


if __name__ == '__main__':
    ascyncio.run(main())