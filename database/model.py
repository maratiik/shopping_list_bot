from sqlalchemy import String, Integer, Boolean

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class Base(DeclarativeBase):

    pass


class Item(Base):

    __tablename__ = 'items'

    id: Mapped[int] = mapped_column(primary_key=True)
    chat_id: Mapped[int] = mapped_column(Integer())
    name: Mapped[str] = mapped_column(String())
    url: Mapped[str] = mapped_column(String(), default='')
    priority: Mapped[int] = mapped_column(Integer(), default=0)
    checked: Mapped[bool] = mapped_column(Boolean(), default=False)


class Favourite(Base):

    __tablename__ = 'favourites'

    id: Mapped[int] = mapped_column(primary_key=True)
    chat_id: Mapped[int] = mapped_column(Integer())
    name: Mapped[str] = mapped_column(String())
    url: Mapped[str] = mapped_column(String(), default='')
    priority: Mapped[int] = mapped_column(Integer(), default=0)
    checked: Mapped[bool] = mapped_column(Boolean(), default=False)
