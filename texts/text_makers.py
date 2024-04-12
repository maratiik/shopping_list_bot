from database.item_data import ItemData
from texts.texts import ITEM_CB, ADD_TO_FAV_CB
from texts.texts import ADD_PRIRORITY_CB, HTTP

import logging

logging.basicConfig(
    level=logging.DEBUG,
    filename='log.log',
    format='%(asctime)s %(levelname)s %(message)s'
)

# texts
def get_item_text_general(item: ItemData) -> str:
    return f"▾ {item.name} {item.priority * '❕'} {item.is_fav * '⭐️'} {item.checked * '☑️'}"


def get_item_text_detail(item: ItemData) -> str:
    return f"▴ {item.name} {item.priority * '❕'} {item.is_fav * '⭐️'} {item.checked * '☑️'}"


def get_item_text_deleting(item: ItemData) -> str:
    return f"{item.name} {item.checked * '☑️'}"


def get_item_url(item: ItemData) -> str:
    return item.url if len(item.url) else None


# callbacks
def get_item_cb(item: ItemData) -> str:
    return f"{ITEM_CB}{item.name}{item.url}"


def get_item_add_to_fav_cb(item: ItemData) -> str:
    return f"{ADD_TO_FAV_CB}{item.name}"


def get_item_add_priority_cb(item: ItemData) -> str:
    return f"{ADD_PRIRORITY_CB}{item.name}"


def split_url(item_data: str) -> tuple[str, str]:
    name = ''
    url = ''
    if HTTP in item_data:
        name = item_data[:item_data.find(HTTP)]
        url = item_data[item_data.find(HTTP):]
    else:
        name = item_data

    logging.debug(f"split_url() called, name:{name}, url:{url}")

    return name, url
