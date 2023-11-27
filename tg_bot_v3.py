import telebot
import os
from telebot import types
from settings import *
from sqlalchemy import create_engine, select, desc, delete, update
from sqlalchemy.orm import sessionmaker
from db import Item
from app import APP_PATH


###########################
##### Import database #####
###########################


engine = create_engine('sqlite:///' + os.path.join(APP_PATH, 'shopping_list.db'))
Session = sessionmaker(bind=engine)
session = Session()


#####################
##### Functions #####
#####################


def get_items():
    # 0 - name
    # 1 - url
    # 2 - priority
    # 3 - checked

    query = select(Item.name, Item.url, Item.priority, Item.checked).order_by(desc(Item.priority))
    items = session.execute(query)
    items_list = [row for row in items]
    return items_list


def help_keyboard():
    btn_back = types.InlineKeyboardButton(BACK_TEXT, callback_data=BACK)
    markup = types.InlineKeyboardMarkup()
    markup.add(btn_back)
    return markup


def add_keyboard():
    btn_back = types.InlineKeyboardButton(BACK_TEXT, callback_data=BACK)
    markup = types.InlineKeyboardMarkup()
    markup.add(btn_back)
    return markup


def list_keyboard():
    items = get_items()

    markup = types.InlineKeyboardMarkup(
        keyboard=[
            [
                types.InlineKeyboardButton(
                    text=i[0] + ' ' + i[2] * '❗️',
                    callback_data=i[0],
                    url=i[1]
                )
            ]
            for i in items
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


def remove_keyboard():
    items = get_items()

    markup = types.InlineKeyboardMarkup()

    for i in items:
        if i[3]:
            text = i[0] + i[2] * '❗️' + '☑️'
            cb_data = f'checked_{i[0]}'
        else:
            text = i[0] + i[2] * '❗️'
            cb_data = f'notchecked_{i[0]}'

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
    items = get_items()
    keyboard = remove_keyboard()

    if len(items) == 0:
        bot.answer_callback_query(call.id, 'Список очищен!')
        bot.edit_message_reply_markup(
            call.message.chat.id,
            call.message.message_id,
            reply_markup=menu_keyboard()
        )
    else:
        bot.edit_message_reply_markup(
            call.message.chat.id,
            call.message.message_id,
            reply_markup=keyboard
        )


def update_list_keyboard(call):
    keyboard = list_keyboard()
    bot.edit_message_reply_markup(
        call.message.chat.id,
        call.message.message_id,
        reply_markup=keyboard
    )


def remove_checked_items():
    delete_condition = Item.checked == True
    query = delete(Item).where(delete_condition)

    session.execute(query)
    session.commit()


def remove_all():
    query = delete(Item)
    session.execute(query)
    session.commit()


def add_items(message):
    global adding

    if adding:
        adding = False
        return message.text
    return None


def check_uncheck(item_name, set_to):
    update_condition = Item.name == item_name
    query = update(Item).where(update_condition).values(checked=set_to)
    session.execute(query)
    session.commit()


def add_priority(item_name):
    current_priority = session.query(Item.priority).filter(Item.name == item_name).scalar()
    new_priority = (current_priority + 1) % 4

    query = update(Item).where(Item.name == item_name).values(priority=new_priority)
    session.execute(query)
    session.commit()



#####################
##### Variables #####
#####################


adding = False

bot = telebot.TeleBot(TOKEN)


############################
##### Message handlers #####
############################


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        'Меню',
        reply_markup=menu_keyboard()
    )


@bot.message_handler(func=add_items)
def add_to_list(message):
    items = message.text.split(sep=', ')

    for item in items:
        item_url = ''

        if HTTP in item:
            item_name = item[:item.find(HTTP)-1]
            item_url = item[item.find(HTTP):]
        else:
            item_name = item

        data = Item(name=item_name, url=item_url)
        session.add(data)
        session.commit()

    bot.reply_to(message, 'Добавлено!')

    bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=message_to_edit,
        text='Меню',
        reply_markup=menu_keyboard()
    )


##################################
##### Callback query handler #####
##################################


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    global adding
    items = get_items()

    if call.data == LIST:
        if len(items) == 0:
            bot.answer_callback_query(
                call.id,
                'Список пуст!'
            )
        else:
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text='Список',
                reply_markup=list_keyboard()
            )

    elif call.data == BACK:
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text='Меню',
            reply_markup=menu_keyboard()
        )
        adding = False

    elif call.data == ADD:
        global message_to_edit
        message_to_edit = call.message.message_id

        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text='Что добавить?',
            reply_markup=add_keyboard())

        adding = True

    elif call.data == REMOVE:
        if len(items) == 0:
            bot.answer_callback_query(
                call.id,
                'Нечего удалять!'
            )
        else:
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text='Удаляем-с',
                reply_markup=remove_keyboard()
            )

    elif call.data.startswith('checked_'):
        item_name = call.data.split('_', 1)[1]
        check_uncheck(item_name, False)

    elif call.data.startswith('notchecked_'):
        item_name = call.data.split('_', 1)[1]
        check_uncheck(item_name, True)

    elif call.data == REMOVE_CHECKED:
        remove_checked_items()
        update_remove_keyboard(call)
        bot.answer_callback_query(
            call.id,
            'Вроде удалил'
        )

    elif call.data == REMOVE_ALL:
        remove_all()
        update_remove_keyboard(call)
        bot.answer_callback_query(
            call.id,
            'Все удалено!'
        )

    elif call.data == HELP:
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=HELP_MESSAGE,
            reply_markup=help_keyboard()
        )

    for item in items:
        if call.data == item[0]:
            add_priority(item[0])
            update_list_keyboard(call)


bot.infinity_polling()