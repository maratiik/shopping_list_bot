import telebot
from telebot import types
import re

bot = telebot.TeleBot('6489686700:AAGvaOAVkzLrxM3naxmXYHgD98snoi3784Q')

shopping_list = [1, 2, 3]

@bot.callback_query_handler()

@bot.message_handler(regexp='/.*')
def execute(message):
    print('yoyo')
    markup = types.InlineKeyboardMarkup(row_width=1)
    # button1 = types.InlineKeyboardButton('a', callback_data='yo')
    # button2 = types.InlineKeyboardButton('b', callback_data='hua')
    for i in range(5):
        markup.add(types.InlineKeyboardButton(f'{i}', callback_data=f'{i}'))
    markup.add(types.InlineKeyboardButton('Edit', callback_data='edit'),)
    bot.send_message(message.chat.id, 'hello', reply_markup=markup)



bot.infinity_polling()