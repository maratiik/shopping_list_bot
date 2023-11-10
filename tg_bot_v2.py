import re
import pickle
import telebot
from telebot import types
import pathlib


PICKLE_SL = pathlib.Path('shopping_list.pickle').resolve()
PICKLE_IB = pathlib.Path('item_buttons.pickle').resolve()
TOKEN = '6489686700:AAGvaOAVkzLrxM3naxmXYHgD98snoi3784Q'

ADD = 'add'
ADD_TEXT = 'Добавить'
ADD_CANCEL = 'add_cancel'
ADD_CANCEL_TEXT = 'Отменить добавление'

LIST = 'list'
LIST_TEXT = 'Посмотреть список'

REMOVE = 'remove'
REMOVE_TEXT = 'Удалить'

BACK = 'back'
BACK_TEXT = 'Назад'

HTTP = 'http'

bot = telebot.TeleBot(TOKEN)

class Item:
    def __init__(self, name, url = ''):
        self.name = name
        self.url = url
        self.markdown_name = ''

        if len(url) != 0:
            self.markdown_name = f'[{name}]({url})'

a = Item(name='вебка',
        url = 'https://market.yandex.ru/product--veb-kamera-logitech-c922-pro-stream-chernyi/1711878907?sku=100328764984&offerid=2etY_X3bFIS7sAqazrpjGA&cpc=-xilxGNuDdkIz0uRUJFweeAcHQRyO9dxUIlWcCsVilesDF6E9RXpmMunWFWJ3sMP4zULVhq3lwMLJsHIv1iib20sLKXDYsiphwCcA_H0kGJjRM6-bOSck0qpepJGSSA7lTrbK_AelkT4hWop4zXK2Zo2UnF1nKBABhoElZnfJphsNgCdX5ZTsRNWiMggL4N6oJclO834oz2XGajl8Zq8Iw,,&show-uid=16996193774081571756909009&lr=172&')
b = Item(name='картошка')
c = Item(name='Масло')

def unpickle_sl():
    if PICKLE_SL.exists():
        with open(PICKLE_SL, 'rb') as f:
            uploaded_list = pickle.load(f)
        return uploaded_list
    return []

def unpickle_ib():
    if PICKLE_IB.exists():
        with open(PICKLE_IB, 'rb') as f:
            uploaded_list = pickle.load(f)
        return uploaded_list
    return []

#shopping_list = unpickle_sl()
shopping_list = [a, b, c]
menu = {ADD: ADD_TEXT, LIST: LIST_TEXT, REMOVE: REMOVE_TEXT}

def list_keyboard():
    markup = types.InlineKeyboardMarkup(
        keyboard=[
            [
                types.InlineKeyboardButton(
                    text=item.name,
                    callback_data=item.name
                )
            ]
            for item in shopping_list
        ]
    )
    markup.add(types.InlineKeyboardButton(
        text=BACK_TEXT,
        callback_data=BACK
    ))
    return markup

def menu_keyboard():
    return types.InlineKeyboardMarkup(
        keyboard=[
            [
                types.InlineKeyboardButton(
                    text=menu[key],
                    callback_data=key
                )
            ]
            for key in menu
        ]
    )

def edit_keyboard():
    return types.InlineKeyboardMarkup(
        keyboard=[
            [
                types.InlineKeyboardButton(
                text=BACK_TEXT,
                callback_data=BACK
            )
            ]
        ]
    )

def process_text(text):
    items_list = text.split(sep=', ')
    items_dict = {}

    for i in range(len(items_list)):
        if not HTTP in items_list[i]:
            items_dict[items_list[i]] = ''
        if HTTP in items_list[i]:
            items_dict[items_list[i-1]] = items_list[i]
    return items_dict


@bot.message_handler(commands=['start'])
def execute(message):
    print('started')
    bot.send_message(message.chat.id, 'Меню', reply_markup=menu_keyboard())

@bot.callback_query_handler(func=lambda call: call.data == LIST)
def list_callback(call):
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text='Список', reply_markup=list_keyboard())

@bot.callback_query_handler(func=lambda call: call.data == BACK)
def back_callback(call):
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text='Меню', reply_markup=menu_keyboard())

@bot.callback_query_handler(func=lambda call: call.data == ADD)
def add_callback(call):
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text='Что добавить?', reply_markup=edit_keyboard())
    @bot.message_handler(func=lambda message: True)
    def add_item(message):
        print(f'You added {message.text}')
        #answer_text = process_text(message.text)
        bot.answer_callback_query()
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text='Меню', reply_markup=menu_keyboard())


bot.infinity_polling()
