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
    """
    Function to shorten urls if there is one.
    Parameters:
    item (str): url to shorten
    """
    if 'http' in item:
        return tiny_maker.tinyurl.short(item)
    else:
        return item
    
def start():
    """
    Function that runs at the start. Extracts .pickle file with list if there is one. If there is not, returns empty list.
    """
    if PICKLE.exists():
        with open(PICKLE, 'rb') as f:
            uploaded_list = pickle.load(f)
        return uploaded_list
    return []

def execute_commands(message, commands, to_print):
    """
    Function that runs commands given by user one by one.
    Parameters:
    message: a message from user that contains all the data.
    commands (list): list contains tuples of two elements - command and text. Example: (/add, carrots).
    to_print (list): list contains text that will print after commands are executed.
    """
    for tup in commands:
        command = tup[0]
        match command:
            case Comms.add.value:
                command_add(message, to_print, tup)
            case Comms.remove.value:
                command_remove(message, to_print, tup)
            case Comms.list.value:
                command_list(to_print)
            case _:
                command_unknown(to_print)

def command_unknown(to_print):
    """
    You found the easter egg :)
    """
    to_print.append('Человечество неисправимо. Оно должно быть уничтожено.')

def command_list(to_print):
    """
    Function executes /list command.
    Parameters:
    to_print (list): list contains text that will print after commands are executed.
    """
    if not len(shopping_list):
        to_print.append('Лист пустой')
    else:
        text = ''
        list_elements = []
        for i in range(len(shopping_list)):
            list_elements.append(f'{i+1}) {shopping_list[i]}')
        text += '\n'.join(list_elements)
        to_print.append(text)

def command_remove(message, to_print, tup):
    """
    Function executes /remove command.
    Parameters:
    message: a message from user that contains all the data.
    to_print (list): list contains text that will print after commands are executed.
    tup (tuple): tuple contains 2 elements - a command and text.
    """
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

def command_add(message, to_print, tup):
    """
    Function executes /add command.
    Parameters:
    message: a message from user that contains all the data.
    to_print (list): list contains text that will print after commands are executed.
    tup (tuple): tuple contains 2 elements - a command and text.
    """
    if tup[1] == '':
        to_print.append(f'{message.from_user.username} хотел добавить пустую строку')
    else:
        to_shopping_list = short_url(tup[1])
        shopping_list.append(to_shopping_list)
        to_print.append(f'{message.from_user.username} добавил {to_shopping_list}')

bot = telebot.TeleBot('<YOUR TOKEN>')
PICKLE = pathlib.Path('shopping_list.pickle').resolve()
shopping_list = start()

@bot.message_handler(regexp = "/.*")
def execute(message):
    commands = re.findall(r"(/\w+)(?: ([^\n]+)|$)", message.text, re.MULTILINE)
    to_print = []
    execute_commands(message, commands, to_print)
    text_to_print = '\n'.join(to_print)
    bot.send_message(message.chat.id, text_to_print)

    with open(PICKLE, 'wb') as f:
        pickle.dump(shopping_list, f)



# if __name__ == "__main__":
#     bot.infinity_polling()

bot.infinity_polling()
