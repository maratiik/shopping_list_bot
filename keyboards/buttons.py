from aiogram.types import InlineKeyboardButton
from texts import texts
from texts import text_makers as tm
from database.item_data import ItemData


def btn_back() -> InlineKeyboardButton:
    return InlineKeyboardButton(
        text=texts.BACK_TEXT,
        callback_data=texts.BACK_CB
    )


def btns_item_detail(item: ItemData) -> list[InlineKeyboardButton]:
    btns = []

    if tm.get_item_url(item):
        btns.append(InlineKeyboardButton(
            text=texts.GO_URL_TEXT,
            url=tm.get_item_url(item),
            callback_data=tm.get_item_cb(item)
        ))

    btns.append(InlineKeyboardButton(
        text=texts.ADD_PRIRORITY_TEXT,
        # callback_data=tm.get_item_add_priority_cb(item)
        callback_data=texts.ADD_PRIRORITY_CB
    ))

    btns.append(InlineKeyboardButton(
        text=texts.ADD_TO_FAV_TEXT,
        # callback_data=tm.get_item_add_to_fav_cb(item)
        callback_data=texts.ADD_TO_FAV_CB
    ))

    return btns


def btns_delete() -> list[InlineKeyboardButton]:
    return [
        InlineKeyboardButton(
            text=texts.DELETE_CHECKED_TEXT,
            callback_data=texts.DELETE_CHECKED_CB
        ),
        InlineKeyboardButton(
            text=texts.DELETE_ALL_TEXT,
            callback_data=texts.DELETE_ALL_CB
        )
    ]