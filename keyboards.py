from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
import asyncio
from texts import *
from model import ItemData

def menu_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for key in menu_keys.keys():
        builder.add(InlineKeyboardButton(text=menu_keys[key],
                                         callback_data=key))
    builder.adjust(1)
    return builder.as_markup()


def keyboard_from_items(items: list[ItemData], removing: bool) -> InlineKeyboardMarkup:
    if removing:
        builder = InlineKeyboardBuilder()
        for item in items:
            builder.add(InlineKeyboardButton(text=make_item_text(item, removing=True),
                                             url=make_item_url(item),
                                             callback_data=make_item_cb_removing(item)))
        builder.add(InlineKeyboardButton(text=REMOVE_CHECKED_TEXT,
                                         callback_data=REMOVE_CHECKED_CB))
        builder.add(InlineKeyboardButton(text=REMOVE_ALL_TEXT,
                                         callback_data=REMOVE_ALL_CB))
        builder.add(btn_back())
        builder.adjust(1)
        return builder.as_markup()
    builder = InlineKeyboardBuilder()
    for item in items:
        builder.add(InlineKeyboardButton(text=make_item_text(item),
                                         url=make_item_url(item),
                                         callback_data=make_item_cb(item)))
    builder.add(btn_back())
    builder.adjust(1)
    return builder.as_markup()


def back_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(btn_back())
    return builder.as_markup()


def btn_back() -> InlineKeyboardButton:
    return InlineKeyboardButton(
        text=BACK_TXT,
        callback_data=BACK_CB
    )


# item = (name, quantity, url, priority, checked)
def make_item_text(item: ItemData, removing: bool = False) -> str:
    if removing:
        if item.quantity > 1:
            return f"{item.name} x{item.quantity} {item.checked * '☑️'}"
        return f"{item.name} {item.checked * '☑️'}"

    if item.quantity > 1:
        return f"{item.name} x{item.quantity} {item.priority * '❕'}"
    return f"{item.name} {item.priority * '❕'}"


def make_item_url(item: ItemData) -> str:
    return item.url


def make_item_cb_removing(item: ItemData) -> str:
    return f"checked_{item.name}" if item.checked == True else f"notchecked_{item.name}"


def make_item_cb(item: tuple) -> str:
    return f"item_{item.name}"