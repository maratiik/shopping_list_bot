from typing import NamedTuple


class ItemData(NamedTuple):

    name: str
    url: str = ''
    priority: int = 0
    checked: bool = False
    is_fav: bool = False

if __name__ == '__main__':
    a = ItemData(
        name='asdasd',
        url='qqq',
        is_fav=True
    )
    print(a)
