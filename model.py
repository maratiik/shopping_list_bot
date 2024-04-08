from typing import NamedTuple
import abc

from sqlalchemy import create_engine, String, Integer, Boolean
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session
from sqlalchemy import select


#TODO: пункт 1

class ItemData(NamedTuple):

    name: str
    quantity: int
    url: str
    priority: int
    checked: bool


class FavouriteData(NamedTuple):

    name: str
    url: str
    checked: bool


def fav_to_item(fav_item: FavouriteData) -> ItemData:
    return ItemData(fav_item.name, 1, fav_item.url, 0, False)


def item_to_fav(item: ItemData) -> FavouriteData:
    return FavouriteData(item.name, item.url, False)


class Base(DeclarativeBase):

    pass


class Item(Base):

    __tablename__ = 'items'

    id: Mapped[int] = mapped_column(primary_key=True)
    chat_id: Mapped[int] = mapped_column(Integer())
    name: Mapped[str] = mapped_column(String(30))
    quantity: Mapped[int] = mapped_column(Integer(), default=1)
    url: Mapped[str] = mapped_column(String(100))
    priority: Mapped[int] = mapped_column(Integer(), default=0)
    checked: Mapped[bool] = mapped_column(Boolean(), default=False)


class Favourite(Base):

    __tablename__ = 'favourites'

    id: Mapped[int] = mapped_column(primary_key=True)
    chat_id: Mapped[int] = mapped_column(Integer())
    name: Mapped[str] = mapped_column(String(30))
    url: Mapped[str] = mapped_column(String(100))
    checked: Mapped[bool] = mapped_column(Boolean(), default=False)
