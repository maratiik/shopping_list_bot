from telebot import types
import pickle
import constants

class BotLoader:
    '''
    Pickler and unpickler
    '''
    def __init__(self):
        self.path = constants.PICKLE
        print(self.path)

    def load(self):
        if self.path.exists():
            with open(self.path, 'rb') as f:
                uploaded_list = pickle.load(f)
            return uploaded_list
        return []

    def save(self, list_to_save):
        with open(self.path, 'wb') as f:
            pickle.dump(list_to_save, f)

class Item:
    '''
    Item container
    '''
    def __init__(self, name, url=None):
        self.name = name
        self.url = url
        self.priority = 1 # from 0 to 3

    def remove_from_list(self, items_list):
        items_list.remove(self)

    def set_priority(self, value):
        self.priority = value

    def get_priority(self):
        return self.priority

class Keyboard:
    def __init__(self):
        self.markup = types.InlineKeyboardMarkup()

    def set_main_keyboard(self):
