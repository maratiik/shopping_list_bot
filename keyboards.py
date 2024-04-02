from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
import asyncio
import texts
from model import ItemData


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
            text=make_item_text(item),
            url=make_item_url(item),
            callback_data=make_item_cb(item)
        ))
    builder.add(btn_back())
    builder.adjust(1)
    return builder.as_markup()


def removing_keyboard_from_items(items: list[ItemData]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for item in items:
        builder.add(
            InlineKeyboardButton(
                text=make_item_text_removing(item),
                callback_data=make_item_cb_removing(item)
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


def make_item_text(item: ItemData) -> str:
    if item.quantity > 1:
        return f"{item.name} x{item.quantity} {item.priority * '❕'}"
    return f"{item.name} {item.priority * '❕'}"


def make_item_text_removing(item: ItemData) -> str:
    if item.quantity > 1:
        return f"{item.name} x{item.quantity} {item.checked * '☑️'}"
    return f"{item.name} {item.checked * '☑️'}"


def make_item_url(item: ItemData) -> str:
    return item.url


def make_item_cb_removing(item: ItemData) -> str:
    return f"checked_{item.name}" if item.checked == True else f"notchecked_{item.name}"


def make_item_cb(item: ItemData) -> str:
    return f"item_{item.name}"
