from typing import List, Optional
from sqlalchemy import create_engine, ForeignKey, String, Integer
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from sqlalchemy.orm import Session
from sqlalchemy import select


class Base(DeclarativeBase):

    pass


class Item(Base):

    __tablename__ = 'items'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    quantity: Mapped[int] = mapped_column(Integer(), default=1)
    url: Mapped[str] = mapped_column(String(100))
    priority: Mapped[int] = mapped_column(Integer(), default=0)
    checked: Mapped[int] = mapped_column(Integer(), default=0)

    def __repr__(self) -> str:
        return f"Item(id={self.id!r}, name={self.name!r}, url={self.url!r}, priority={self.priority!r}, checked={self.checked!r})"


class DataAccessObject:

    def __init__(self, db_url: str):
        self.engine = create_engine(url=db_url)
        
        Base.metadata.create_all(self.engine)

    def save_item(self, item_name: str, item_url: str = '') -> None:
        if not self.exists(item_name):
            with Session(self.engine) as session:
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

    def get_item(self, item_name: str) -> tuple:
        with Session(self.engine) as session:
            return session.query(
                Item.name,
                Item.quantity,
                Item.url,
                Item.priority,
                Item.checked).where(Item.name == item_name).one()
    
    def exists(self, item_name: str) -> bool:
        with Session(self.engine) as session:
            count = session.query(Item.name == item_name).count()
            return True if count > 0 else False
    
    def add_quantity(self, item_name: str) -> None:
        with Session(self.engine) as session:
            session.query(Item).filter(Item.name == item_name).update({'quantity': Item.quantity + 1})
            session.commit()


    def remove_quantity(self, item_name: str) -> None:
        with Session(self.engine) as session:
            item = session.query(Item).filter(Item.name == item_name).one()
            if item.quantity > 1:
                item.quantity -= 1
            else:
                session.delete(item)
            session.commit()

    def add_priority(self, item_name: str) -> None:
        with Session(self.engine) as session:
            item = session.query(Item).filter(Item.name == item_name).update({'priority': (Item.priority + 1) % 4})
            session.commit()

    def check_uncheck(self, item_name: str, set_to: int) -> None:
        with Session(self.engine) as session:
            session.query(Item).filter(Item.name == item_name).update({'checked': set_to})
            session.commit()

    def delete_item(self, item_name: str) -> None:
        with Session(self.engine) as session:
            session.query(Item).filter(Item.name == item_name).delete()
            session.commit()


if __name__ == "__main__":
    url = 'sqlite:///item.db'
    dao = DataAccessObject(url)
    dao.remove_quantity('potato')
    print(dao.get_item('potato'))