from database.item_data import ItemData
from texts import texts

# texts
def get_item_text_general(item: ItemData) -> str:
    return f"🔽 {item.name} {item.priority * '❕'} {item.is_fav * '⭐️'}"


def get_item_text_detail(item: ItemData) -> str:
    return f"🔼 {item.name} {item.priority * '❕'} {item.is_fav * '⭐️'}"


def get_item_text_deleting(item: ItemData) -> str:
    return f"{item.name} {item.checked * '☑️'}"


def get_item_url(item: ItemData) -> str:
    return item.url if len(item.url) else None


# callbacks
def get_item_cb(item: ItemData) -> str:
    return f"{texts.ITEM_CB}{item.name} {item.url}"


def get_item_add_to_fav_cb(item: ItemData) -> str:
    return f"{texts.ADD_TO_FAV_CB}{item.name}"


def get_item_add_priority_cb(item: ItemData) -> str:
    return f"{texts.ADD_PRIRORITY_CB}{item.name}"


def split_url(item_data: str) -> tuple:
    name = ''
    url = ''
    if texts.HTTP in item_data:
        name = item_data[item_data.find(texts.HTTP):]
        url = item_data[:item_data.find(texts.HTTP)]
    
    return name, url


if __name__ == '__main__':
    print(split_url('asdhttp:asf'))