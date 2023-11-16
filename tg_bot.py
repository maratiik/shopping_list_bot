import re
import pickle
import telebot
from telebot import types
import pathlib



##### Constants #####



PICKLE = pathlib.Path('shopping_list.pickle').resolve()
TOKEN = '6489686700:AAGvaOAVkzLrxM3naxmXYHgD98snoi3784Q'

ADD = 'add'
ADD_TEXT = 'Добавить ➕'
ADD_CANCEL_TEXT = 'Вернуться назад 🔙'

LIST = 'list'
LIST_TEXT = 'Посмотреть список 🗒'

REMOVE = 'remove'
REMOVE_TEXT = 'Удалить ➖'

REMOVE_CHECKED = 'remove_checked'
REMOVE_CHECKED_TEXT = 'Удалить отмеченное ➖'

REMOVE_ALL = 'remove_all'
REMOVE_ALL_TEXT = 'Удалить всё ❌'

BACK = 'back'
BACK_TEXT = 'Назад 🔙'

HELP = 'help'
HELP_TEXT = 'Помощь ❓'

HTTP = 'http'

HELP_MESSAGE = '''
- Чтобы добавить что-то, напишите сообщение в виде:
'<наименование 1> <URL 1>, <наименование 2> <URL 2>' (URL необязателен);
- Чтобы удалить что-то, выберите это в списке пункта 'Удалить', затем нажмите 'Удалить отмеченное';
- Чтобы удалить все сразу, нажмите 'Удалить все' в пункте 'Удалить';
- Чтобы поменять приоритет закупки, нажмите на ее название в общем списке.
'''

##### Item class #####



class Item:
    '''
    Contains items' NAME, URL and MARKDOWN NAME
    '''
    def __init__(self, name, url = None):
        self.name = name
        self.url = url
        self.priority = 0 # from 0 to 3

    def remove_from_list(self, item_list):
        item_list.remove(self)

    def add_priority(self):
        if self.priority < 3:
            self.priority += 1
        else:
            self.priority = 0



##### Functions #####



def unpickle_sl():
    '''
    Restores shopping_list from pickle
    '''
    if PICKLE.exists():
        with open(PICKLE, 'rb') as f:
            uploaded_list = pickle.load(f)
        return uploaded_list
    return []

def pickle_sl():
    '''
    Pickles shopping_list
    '''
    with open(PICKLE, 'wb') as f:
        pickle.dump(shopping_list, f)

def sort_list():
    return sorted(shopping_list, key=lambda item: item.priority, reverse=True)

def add_keyboard():
    '''
    Draws ADD keyboard:

    Что хотите добавить?
    BACK

    '''
    btn_back = types.InlineKeyboardButton(BACK_TEXT, callback_data=BACK)
    markup = types.InlineKeyboardMarkup()
    markup.add(btn_back)
    return markup

def help_keyboard():
    '''
    Draws HELP keyboard

    *help*
    BACK

    '''
    btn_back = types.InlineKeyboardButton(BACK_TEXT, callback_data=BACK)
    markup = types.InlineKeyboardMarkup()
    markup.add(btn_back)
    return markup


def list_keyboard():
    '''
    Draws LIST keyboard:

    item1
    item2
    item3
    BACK

    '''
    markup = types.InlineKeyboardMarkup(
        keyboard=[
            [
                types.InlineKeyboardButton(
                    text=item.name + ' ' + item.priority * '❗️',
                    callback_data=item.name,
                    url=item.url
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
    '''
    Draws MENU keyboard:

    ADD
    LIST
    REMOVE
    HELP

    '''
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

def remove_keyboard():
    '''
    Draws REMOVE keyboard:

    item1
    item2
    item3
    REMOVE CHECKED
    BACK

    '''
    markup = types.InlineKeyboardMarkup()

    for item in shopping_list:
        if item.name in checked_items:
            text = item.name + ' ' + item.priority * '❗️' + ' ☑️'
            cb_data = f'checked_{item.name}'
            #print(type(text))
        else:
            text = item.name + ' ' + item.priority * '❗️'

            cb_data = f'notchecked_{item.name}'

        markup.add(types.InlineKeyboardButton(
            text=text,
            callback_data=cb_data
        ))

    markup.add(types.InlineKeyboardButton(
        text=REMOVE_CHECKED_TEXT,
        callback_data=REMOVE_CHECKED
    ))
    markup.add(types.InlineKeyboardButton(
        text=REMOVE_ALL_TEXT,
        callback_data=REMOVE_ALL
    ))
    markup.add(types.InlineKeyboardButton(
        text=BACK_TEXT,
        callback_data=BACK
    ))
    return markup

def update_remove_keyboard(call):
    '''
    Updated remove_keyboard, usually after removing items
    '''
    keyboard = remove_keyboard()
    if len(shopping_list) == 0:
        bot.answer_callback_query(call.id, 'Список очищен!')
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=menu_keyboard())
    else:
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=keyboard)

def update_list_keyboard(call):
    keyboard = list_keyboard()
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=keyboard)

def remove_checked_items():
    '''
    Removes checked items from shopping_list
    '''
    for item_name in checked_items.copy():
        for item in shopping_list:
            if item.name == item_name:
                item.remove_from_list(shopping_list)
                pickle_sl()

def add_items(message):
    '''
    Adds items to shopping_list
    '''
    global adding

    if adding:
        adding = False
        return message.text
    return None



##### Some global variables #####



adding = False

bot = telebot.TeleBot(TOKEN)

shopping_list = unpickle_sl()
#shopping_list = []
checked_items = []
menu = {ADD: ADD_TEXT, LIST: LIST_TEXT, REMOVE: REMOVE_TEXT, HELP: HELP_TEXT}



##### Message handlers #####



@bot.message_handler(commands=['start'])
def execute(message):
    '''
    Starts bot by showing MENU keyboard
    '''
    bot.send_message(message.chat.id, 'Меню', reply_markup=menu_keyboard())

@bot.message_handler(func = add_items)
def add(message):
    '''
    Reads items from User and adds them to shopping_list
    '''
    items_list = message.text.split(sep=', ')
    for item in items_list:
        item_url = ''
        if HTTP in item:
            item_name = item[:item.find(HTTP)-1]
            item_url = item[item.find(HTTP):]
        else:
            item_name = item
        product = Item(item_name, item_url)
        shopping_list.append(product)
    #bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id,
    #                      text='Меню', reply_markup=menu_keyboard())
    bot.reply_to(message, 'Добавлено!')
    bot.edit_message_text(chat_id=message.chat.id, message_id=message_to_edit,
                          text='Меню', reply_markup=menu_keyboard())



##### Callback query handler #####



@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    '''
    Checks which buttons are clicked
    '''
    global adding
    global shopping_list

    if call.data == LIST:
        if len(shopping_list) == 0:
            bot.answer_callback_query(call.id, 'Список пуст!')
        else:
            shopping_list = sort_list()
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='Список', reply_markup=list_keyboard())

    elif call.data == BACK:
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text='Меню', reply_markup=menu_keyboard())
        adding = False

    elif call.data == ADD:
        global message_to_edit
        message_to_edit = call.message.message_id

        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text='Что добавить?', reply_markup=add_keyboard())

        adding = True

    elif call.data == REMOVE:
        if len(shopping_list) == 0:
            bot.answer_callback_query(call.id, 'Нечего удалять!')
        else:
            shopping_list = sort_list()
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='Удаляем-с', reply_markup=remove_keyboard())

    elif call.data.startswith('checked_'):
        item_name = call.data.split('_', 1)[1]
        checked_items.remove(item_name)
        update_remove_keyboard(call)

    elif call.data.startswith('notchecked_'):
        item_name = call.data.split('_', 1)[1]
        checked_items.append(item_name)
        update_remove_keyboard(call)

    elif call.data == REMOVE_CHECKED:
        if len(checked_items) != 0:
            remove_checked_items()
            checked_items.clear()
            update_remove_keyboard(call)
            bot.answer_callback_query(call.id, 'Готово!')
        else:
            bot.answer_callback_query(call.id, 'Ничего не выделено!')

    elif call.data == REMOVE_ALL:
        shopping_list.clear()
        checked_items.clear()
        update_remove_keyboard(call)
        bot.answer_callback_query(call.id, 'Всё удалено!')

    elif call.data == HELP:
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=HELP_MESSAGE, reply_markup=help_keyboard())

    for item in shopping_list:
        if call.data == item.name:
            item.add_priority()
            update_list_keyboard(call)

    pickle_sl()

bot.infinity_polling()
