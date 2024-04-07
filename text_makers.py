from model import ItemData
import texts

def make_item_text_general(item: ItemData) -> str:
    if item.quantity > 1:
        return f"🔽 {item.name} x{item.quantity} {item.priority * '❕'} {item.starred * '⭐️'}"
    return f"🔽 {item.name} {item.priority * '❕'} {item.starred * '⭐️'}"


def make_item_text_detail(item: ItemData) -> str:
    if item.quantity > 1:
        return f"🔼 {item.name} x{item.quantity} {item.priority * '❕'} {item.starred * '⭐️'}"
    return f"🔼 {item.name} {item.priority * '❕'} {item.starred * '⭐️'}"


def make_item_text_removing(item: ItemData) -> str:
    if item.quantity > 1:
        return f"{item.name} x{item.quantity} {item.checked * '☑️'}"
    return f"{item.name} {item.checked * '☑️'}"


def make_item_text_removing_fav(item: ItemData) -> str:
    if item.quantity > 1:
        return f"{item.name} x{item.quantity} {item.checked_fav * '☑️'}"
    return f"{item.name} {item.checked_fav * '☑️'}"


def make_item_url(item: ItemData) -> str | None:
    return item.url if len(item.url) else None


def make_item_cb_removing(item: ItemData) -> str:
    return f"{texts.CHECKED_CB}{item.name}" if item.checked else f"{texts.NOTCHECKED_CB}{item.name}"


def make_item_cb_removing_fav(item: ItemData) -> str:
    return f"{texts.CHECKED_FAV_CB}{item.name}" if item.checked_fav else f"{texts.NOTCHECKED_FAV_CB}{item.name}"


def make_item_cb(item: ItemData) -> str:
    return f"{texts.ITEM_CB}{item.name}"


def make_item_star_cb(item: ItemData) -> str:
    return f"{texts.STAR_CB}{item.name}"


def make_item_priority_cb(item: ItemData) -> str:
    return f"{texts.ADD_PRIRORITY_CB}{item.name}"