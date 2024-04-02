from sqlalchemy.orm import Session
from sqlalchemy import select, desc

from model import Item, ItemData

import abc
from typing import NamedTuple


class AbstractDAO(abc.ABC):

    @abc.abstractmethod
    def save(self, *args, **kwargs) -> None:
        '''Save entity to db'''

    @abc.abstractmethod
    def get_one(self, name: str) -> NamedTuple:
        '''Get one entity from db'''

    @abc.abstractmethod
    def get_all(self) -> list[NamedTuple]:
        '''Get all entities from db'''

    @abc.abstractmethod
    def exists(self, name: str) -> bool:
        '''Returns true if entity exists'''

    @abc.abstractmethod
    def delete_one(self, name: str) -> None:
        '''Delete one entity from db'''

    @abc.abstractmethod
    def delete_all(self) -> None:
        '''Delete all entities from db'''

    
class ItemDAO(AbstractDAO):

    def __init__(self, session: Session) -> None:
        self.session = session

    def save(self, item_name: str, item_url: str = '') -> None:
        if not self.exists(item_name):
            item = Item(
                name=item_name,
                quantity=1,
                url=item_url,
                priority=0,
                checked=0
            )
            self.session.add(item)
            self.session.commit()
        else:
            self.add_quantity(item_name)

    def get_one(self, item_name: str) -> ItemData:
        result = self.session.query(
            Item.name,
            Item.quantity,
            Item.url,
            Item.priority,
            Item.checked
        ).where(Item.name == item_name).one()
        return ItemData(*result)

    def get_all(self) -> list[ItemData]:
        result = self.session.query(
            Item.name,
            Item.quantity,
            Item.url,
            Item.priority,
            Item.checked
        ).order_by(desc(Item.priority)).all()
        return [ItemData(*item) for item in result]

    def exists(self, item_name: str) -> bool:
        return self.session.query(Item.id).filter_by(name=item_name).first() is not None

    def delete_one(self, item_name: str) -> None:
        self.session.query(Item).filter(Item.name == item_name).delete()
        self.session.commit()

    def delete_all(self) -> None:
        self.session.query(Item).delete()
        self.session.commit()

    def add_quantity(self, item_name: str) -> None:
        self.session.query(Item).filter(Item.name == item_name).update({'quantity': Item.quantity + 1})
        self.session.commit()

    def remove_quantity(self, item_name: str) -> None:
        item = self.session.query(Item).filter(Item.name == item_name).one()
        if item.quantity > 1:
            item.quantity -= 1
        else:
            self.session.delete(item)
        self.session.commit()

    def add_priority(self, item_name: str) -> None:
        self.session.query(Item).filter(Item.name == item_name).update({'priority': (Item.priority + 1) % 4})
        self.session.commit()

    def check_uncheck(self, item_name: str, set_to: bool) -> None:
        self.session.query(Item).filter(Item.name == item_name).update({'checked': set_to})
        self.session.commit()
    
    def delete_checked(self) -> None:
        self.session.query(Item).filter(Item.checked == True).delete()
        self.session.commit()
