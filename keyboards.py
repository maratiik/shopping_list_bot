from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import asyncio
from texts import *


def menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                text=key_txt, 
                callback_data=key_cb,
            )
            for key_cb, key_txt in menu_keys
        ]
    ])


def keyboard_from_items(items: list) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                text=make_item_text(item),
                url=make_item_url(item),
                callback_data=make_item_cb(item),
            )
            for item in items
        ]
    ]).add(btn_back())


def btn_back() -> InlineKeyboardButton:
    return InlineKeyboardButton(
        text=BACK_TXT,
        callback_data=BACK_CB
    )


# item = (name, quantity, url, priority, checked)
def make_item_text(item: tuple) -> str:
    return f"{item[0]} {item[3] * '❕'}"


def make_item_url(item: tuple) -> str:
    return item[2]


def make_item_cb(item: tuple) -> str:
    return f"checked_{item[0]}" if item[4] == 1 else f"notchecked_{item[0]}"
