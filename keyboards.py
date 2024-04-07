from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
import asyncio
import texts
from model import ItemData
import text_makers as tm


def menu_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for callback in texts.menu_keys.keys():
        builder.add(InlineKeyboardButton(
            text=texts.menu_keys[callback],
            callback_data=callback
        ))
    builder.adjust(1)
    return builder.as_markup()


def keyboard_from_items(items: list[ItemData]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for item in items:
        builder.add(InlineKeyboardButton(
            text=tm.make_item_text_general(item),
            callback_data=tm.make_item_cb(item)
        ))
    builder.add(btn_back())
    builder.adjust(1)
    return builder.as_markup()


def removing_keyboard_from_items(items: list[ItemData]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for item in items:
        builder.add(
            InlineKeyboardButton(
                text=tm.make_item_text_removing(item),
                callback_data=tm.make_item_cb_removing(item)
            )
        )
    builder.add(InlineKeyboardButton(
        text=texts.REMOVE_CHECKED_TEXT,
        callback_data=texts.REMOVE_CHECKED_CB
    ))
    builder.add(InlineKeyboardButton(
        text=texts.REMOVE_ALL_TEXT,
        callback_data=texts.REMOVE_ALL_CB
    ))
    builder.add(btn_back())
    builder.adjust(1)
    return builder.as_markup()


def back_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(btn_back())
    return builder.as_markup()


def btn_back() -> InlineKeyboardButton:
    return InlineKeyboardButton(
        text=texts.BACK_TXT,
        callback_data=texts.BACK_CB
    )


def item_detail_keyboard(item_name: str, items: list[ItemData]) -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    for item in items:
        if item.name == item_name:
            builder.row(InlineKeyboardButton(
                text=tm.make_item_text_detail(item),
                callback_data=tm.make_item_cb(item)
            ))
            builder.row(*btns_item_detail(item))
        else:
            builder.row(InlineKeyboardButton(
                text=tm.make_item_text_general(item),
                callback_data=tm.make_item_cb(item)
            ))
        
    builder.row(btn_back())
    return builder.as_markup()


def btns_item_detail(item: ItemData) -> list[InlineKeyboardButton]:
    btns = []

    if tm.make_item_url(item):
        btns.append(InlineKeyboardButton(
            text=texts.GO_WEB,
            url=tm.make_item_url(item),
            callback_data=tm.make_item_cb(item)
        ))
    btns.append(InlineKeyboardButton(
        text=texts.ADD_PRIRORITY_TEXT,
        callback_data=tm.make_item_priority_cb(item)
    ))
    btns.append(InlineKeyboardButton(
        text=texts.STAR_TEXT,
        callback_data=tm.make_item_star_cb(item)
    ))
    return btns
