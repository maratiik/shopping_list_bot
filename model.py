from typing import NamedTuple

from sqlalchemy import create_engine, String, Integer, Boolean
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session
from sqlalchemy import select


class ItemData(NamedTuple):

    name: str
    quantity: int
    url: str
    priority: int
    checked: bool


class Base(DeclarativeBase):

    pass


class Item(Base):

    __tablename__ = 'items'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    quantity: Mapped[int] = mapped_column(Integer(), default=1)
    url: Mapped[str] = mapped_column(String(100))
    priority: Mapped[int] = mapped_column(Integer(), default=0)
    checked: Mapped[bool] = mapped_column(Boolean(), default=False)

    def __repr__(self) -> str:
        return f"Item(id={self.id!r}, name={self.name!r}, url={self.url!r}, priority={self.priority!r}, checked={self.checked!r})"  


class DataAccessObject:

    def __init__(self, session: Session) -> None:
        self.session = session

    def save_item(self, item_name: str, item_url: str = '') -> None:
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
            self.session.close()
        else:
            self.add_quantity(item_name)

    def get_item(self, item_name: str) -> ItemData:
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
        ).all()
        return [ItemData(*item) for item in result]
    
    def exists(self, item_name: str) -> bool:
        return self.session.query(Item.id).filter_by(name=item_name).first() is not None
    
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
        item = self.session.query(Item).filter(Item.name == item_name).update({'priority': (Item.priority + 1) % 4})
        self.session.commit()

    def check_uncheck(self, item_name: str, set_to: int) -> None:
        self.session.query(Item).filter(Item.name == item_name).update({'checked': set_to})
        self.session.commit()

    def delete_item(self, item_name: str) -> None:
        self.session.query(Item).filter(Item.name == item_name).delete()
        self.session.commit()

    def remove_checked(self) -> None:
        self.session.query(Item).filter(Item.checked == 1).delete()
        self.session.commit()

    def remove_all(self) -> None:
        self.session.query(Item).delete()
        self.session.commit()


if __name__ == "__main__":
    url = 'sqlite:///item.db'
    dao = DataAccessObject(url, Base)
    dao.create_tables()
    dao.save_item('milk')
    dao.save_item('potato')
    print(dao.get_all())
    