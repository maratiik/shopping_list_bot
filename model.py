from typing import NamedTuple
import abc

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
