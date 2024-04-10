from typing import NamedTuple


class ItemData(NamedTuple):

    name: str
    url: str = ''
    priority: int = 0
    checked: bool = False
    is_fav: bool = False

if __name__ == '__main__':
    a = ItemData(name='abc', url='def', priority=2, checked=False)
    print(a)
    b = ItemData(a.name, a.url, a.priority, a.checked, True)
    print(b)
