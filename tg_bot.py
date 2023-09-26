import re
import pickle
import telebot
import pyshorteners
import pathlib
from enum import Enum

tiny_maker = pyshorteners.Shortener()

class Comms(Enum):
    add = '/add'
    remove = '/remove'
    list = '/list'
    all = 'all'
    empty = ''

def short_url(item):
    if 'http' in item:
        return tiny_maker.tinyurl.short(item)
    else:
        return item
    
def start():
    if PICKLE.exists():
        with open(PICKLE, 'rb') as f:
            uploaded_list = pickle.load(f)
        return uploaded_list
    return []

bot = telebot.TeleBot('<YOUR TOKEN>')
PICKLE = pathlib.Path('shopping_list.pickle').resolve()
shopping_list = start()

@bot.message_handler(regexp = "/.*")
def execute(message):
    commands = re.findall(r"(/\w+)(?: ([^\n]+)|$)", message.text, re.MULTILINE)
    to_print = []
    for tup in commands:
        command = tup[0]
        match command:
            case Comms.add.value:
                if tup[1] == '':
                    bot.send_message(message.chat.id, 'Пустая строка')
                else:
                    to_shopping_list = short_url(tup[1])
                    shopping_list.append(to_shopping_list)
                    to_print.append(f'{message.from_user.username} добавил {to_shopping_list}')
            case Comms.remove.value:
                if not len(shopping_list):
                    to_print.append('А список уже пустой азаза')
                elif tup[1] == Comms.all.value:
                    shopping_list.clear()
                    to_print.append(f'{message.from_user.username} почистил лист')
                elif tup[1] == Comms.empty.value:
                    a = shopping_list.pop(-1)
                    to_print.append(f'{message.from_user.username} удалил {a}')
                else:
                    a = tup[1]
                    shopping_list.remove(tup[1])
                    to_print.append(f'{message.from_user.username} удалил {a}')
            case Comms.list.value:
                if not len(shopping_list):
                    to_print.append('Лист пустой')
                else:
                    text = ''
                    list_elements = []
                    for i in range(len(shopping_list)):
                        list_elements.append(f'{i+1}) {shopping_list[i]}')
                    text += '\n'.join(list_elements)
                    to_print.append(text)
            case _:
                to_print.append('Человечество неисправимо. Оно должно быть уничтожено.')
    text_to_print = '\n'.join(to_print)
    bot.send_message(message.chat.id, text_to_print)

    with open(PICKLE, 'wb') as f:
        pickle.dump(shopping_list, f)

# if __name__ == "__main__":
#     bot.infinity_polling()

bot.infinity_polling()
