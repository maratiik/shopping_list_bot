from typing import List, Optional, NamedTuple
from functools import wraps

from sqlalchemy import create_engine, ForeignKey, String, Integer, Boolean
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


def active_session(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        with Session(self.engine) as session:
            return func(self, session, *args, **kwargs)
    return wrapper


class DataAccessObject:

    def __init__(self, db_url: str, base: Base) -> None:
        self.engine = create_engine(url=db_url)
        self.base = base
        
    def create_tables(self) -> None:
        self.base.metadata.create_all(self.engine)

    @active_session
    def save_item(self, session: Session, item_name: str, item_url: str = '') -> None:
        if not self.exists(item_name):
            item = Item(
                name=item_name,
                quantity=1,
                url=item_url,
                priority=0,
                checked=0
            )
            session.add(item)
            session.commit()
        else:
            self.add_quantity(item_name)

    @active_session
    def get_item(self, session: Session, item_name: str) -> ItemData:
        result = session.query(
            Item.name,
            Item.quantity,
            Item.url,
            Item.priority,
            Item.checked
        ).where(Item.name == item_name).one()
        return ItemData(*result)

    @active_session
    def get_all(self, session: Session) -> list[ItemData]:
        result = session.query(
            Item.name,
            Item.quantity,
            Item.url,
            Item.priority,
            Item.checked
        ).all()
        return [ItemData(*item) for item in result]
    
    @active_session
    def exists(self, session: Session, item_name: str) -> bool:
        return session.query(Item.id).filter_by(name=item_name).first() is not None
    
    @active_session
    def add_quantity(self, session: Session, item_name: str) -> None:
        session.query(Item).filter(Item.name == item_name).update({'quantity': Item.quantity + 1})
        session.commit()

    @active_session
    def remove_quantity(self, session: Session, item_name: str) -> None:
        item = session.query(Item).filter(Item.name == item_name).one()
        if item.quantity > 1:
            item.quantity -= 1
        else:
            session.delete(item)
        session.commit()

    @active_session
    def add_priority(self, session: Session, item_name: str) -> None:
        item = session.query(Item).filter(Item.name == item_name).update({'priority': (Item.priority + 1) % 4})
        session.commit()

    @active_session
    def check_uncheck(self, session: Session, item_name: str, set_to: int) -> None:
        session.query(Item).filter(Item.name == item_name).update({'checked': set_to})
        session.commit()

    @active_session
    def delete_item(self, session: Session, item_name: str) -> None:
        session.query(Item).filter(Item.name == item_name).delete()
        session.commit()

    @active_session
    def remove_checked(self, session: Session) -> None:
        session.query(Item).filter(Item.checked == 1).delete()
        session.commit()

    @active_session
    def remove_all(self, session: Session) -> None:
        session.query(Item).delete()
        session.commit()


if __name__ == "__main__":
    url = 'sqlite:///item.db'
    dao = DataAccessObject(url, Base)
    dao.create_tables()
    dao.save_item('milk')
    dao.save_item('potato')
    print(dao.get_all())
    