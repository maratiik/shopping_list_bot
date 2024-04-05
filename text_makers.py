from model import ItemData

def make_item_text_general(item: ItemData) -> str:
    if item.quantity > 1:
        return f"🔽 {item.name} x{item.quantity} {item.priority * '❕'}"
    return f"🔽 {item.name} {item.priority * '❕'}"


def make_item_text_detail(item: ItemData) -> str:
    if item.quantity > 1:
        return f"🔼 {item.name} x{item.quantity} {item.priority * '❕'}"
    return f"🔼 {item.name} {item.priority * '❕'}"


def make_item_text_removing(item: ItemData) -> str:
    if item.quantity > 1:
        return f"{item.name} x{item.quantity} {item.checked * '☑️'}"
    return f"{item.name} {item.checked * '☑️'}"


def make_item_url(item: ItemData) -> str | None:
    return item.url if len(item.url) else None


def make_item_cb_removing(item: ItemData) -> str:
    return f"checked_{item.name}" if item.checked == True else f"notchecked_{item.name}"


def make_item_cb(item: ItemData) -> str:
    return f"item_{item.name}"
