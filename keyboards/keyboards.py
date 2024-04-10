from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from texts import texts
from texts import text_makers as tm

import keyboards.buttons as btns

from database.item_data import ItemData


def menu_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.add(
        InlineKeyboardButton(
            text=texts.ADD_TEXT,
            callback_data=texts.ADD_CB
        )
    )
    builder.add(InlineKeyboardButton(
            text=texts.LIST_TEXT,
            callback_data=texts.LIST_CB
        )
    )
    builder.add(InlineKeyboardButton(
            text=texts.FAVOURITES_TEXT,
            callback_data=texts.FAVOURITES_CB
        )
    )
    builder.add(InlineKeyboardButton(
            text=texts.DELETE_TEXT,
            callback_data=texts.DELETE_CB
        )
    )
    builder.add(InlineKeyboardButton(
            text=texts.HELP_TEXT,
            callback_data=texts.HELP_CB
        )
    )

    builder.adjust(1)
    
    return builder.as_markup()


def list_keyboard(items: list[ItemData]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for item in items:
        builder.add(InlineKeyboardButton(
            text=tm.get_item_text_general(item),
            callback_data=tm.get_item_cb(item)
        ))

    builder.add(btns.btn_back())

    builder.adjust(1)

    return builder.as_markup()


def delete_keyboard(items: list[ItemData]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for item in items:
        builder.add(InlineKeyboardButton(
            text=tm.get_item_text_deleting(item),
            callback_data=tm.get_item_cb(item)
        ))
    
    for btn in btns.btns_delete():
        builder.add(btn)

    builder.add(btns.btn_back())

    builder.adjust(1)

    return builder.as_markup()


def back_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(btns.btn_back())

    return builder.as_markup()


def item_detail_keyboard(detailed_item: str, items: list[ItemData]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for item in items:
        if item.name == detailed_item:
            builder.row(InlineKeyboardButton(
                text=tm.get_item_text_detail(item),
                callback_data=tm.make_item_cb(item)
            ))
            builder.row(*btns.btns_item_detail(item))
        else:
            builder.row(InlineKeyboardButton(
                text=tm.get_item_text_general(item),
                callback_data=tm.get_item_cb(item)
            ))

    builder.row(btns.btn_back())

    return builder.as_markup()


def adding_keyboard(items: list[ItemData]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for item in items:
        builder.add(InlineKeyboardButton(
            text=tm.get_item_text_general(item),
            callback_data=tm.get_item_cb(item)
        ))

    builder.add(btns.btn_back())
    
    builder.adjust(1)

    return builder.as_markup()
