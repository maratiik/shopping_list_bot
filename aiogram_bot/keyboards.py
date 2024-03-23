from aiogram.types import (ReplyKeyboardMarkup, ReplyKeyboardRemove,
                        KeyboardButton, InlineKeyboardButton,
                        InlineKeyboardMarkup)
from aiogram import types
from ..settings import *
from Model.item import *


def menu_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=menu[key],
                    callback_data=key
                )
            ]
            for key in menu
        ]
    )


def back_keyboard():
    btn_back = InlineKeyboardButton(text=BACK_TEXT, callback_data=BACK)
    kb = InlineKeyboardMarkup().add(btn_back)
    return kb


def list_keyboard():
    items = get_all()
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=item[0] + ' ' + item[2] * '❗️',
                    callback_data=item[0],
                    url=item[1]
                )
            ] for item in items
        ]
    )
    kb.add(InlineKeyboardButton(
        text=BACK_TEXT,
        callback_data=BACK
    ))

    return kb


def remove_keyboard():
    items = get_all()
    kb = InlineKeyboardMarkup()
    for item in items:
        if item[3] == 1:
            text = item[0] + item[2] * '❗️' + '☑️'
            cb_data = f'checked_{item[0]}'
        else:
            text = item[0] + item[2] * '❗️'
            cb_data = f'notchecked_{item[0]}'
        kb.add(InlineKeyboardButton(
            text=text,
            callback_data=cb_data
        ))

    kb.add(InlineKeyboardButton(
        text=REMOVE_CHECKED_TEXT,
        callback_data=REMOVE_CHECKED
    ))
    kb.add(InlineKeyboardButton(
        text=REMOVE_ALL_TEXT,
        callback_data=REMOVE_ALL
    ))
    kb.add(InlineKeyboardButton(
        text=BACK_TEXT,
        callback_data=BACK
    ))
    return kb

