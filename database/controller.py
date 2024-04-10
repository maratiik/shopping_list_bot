from sqlalchemy.orm import Session
from sqlalchemy import desc

from database.model import Item, Favourite
from database.item_data import ItemData


class ItemDAO:

    def __init__(self, session: Session) -> None:
        self.session = session

    def save(self, chat_id: int, item: ItemData) -> None:
        if not self.exists(chat_id, item):
            item_to_save = Item(
                chat_id=chat_id,
                name=item.name,
                url=item.url,
                priority=item.priority,
                checked=item.checked
            )
            self.session.add(item_to_save)
            self.session.commit()
        else:
            pass

    def get_all(self, chat_id: int) -> list[ItemData]:
        result = self.session.query(
            Item.name,
            Item.url,
            Item.priority,
            Item.checked,
        ).filter(
            Item.chat_id == chat_id
        ).order_by(desc(Item.priority)).all()

        return [ItemData(*item) for item in result]

    def get_all_with_fav_data(self, chat_id: int) -> list[ItemData]:
        result = self.session.query(
            Item.name,
            Item.url,
            Item.priority,
            Item.checked
        ).filter(
            Item.chat_id == chat_id
        ).order_by(desc(Item.priority)).all()

        data = []

        for item in result:
            favDAO = FavouriteDAO(self.session)
            is_in_fav = favDAO.exists(
                chat_id=chat_id,
                item=ItemData(item[0], item[1], item[2], item[3])
            )
            data.append(ItemData(*item), is_in_fav)

        return data

    def delete_checked(self, chat_id: int) -> None:
        self.session.query(Item).filter(
            Item.checked == True,
            Item.chat_id == chat_id,
        ).delete()
        self.session.commit()

    def delete_all(self, chat_id: int) -> None:
        self.session.query(Item).filter(
            Item.chat_id == chat_id
        ).delete()
        self.session.commit()

    def toggle_check(self, chat_id: int, item: ItemData) -> None:
        self.session.query(Item).filter(
            Item.name == item.name,
            Item.chat_id == chat_id
        ).update({'checked': not Item.checked})
        self.session.commit()

    def add_priority(self, chat_id: int, item: ItemData) -> None:
        self.session.query(Item).filter(
            Item.name == item.name,
            Item.chat_id == chat_id,
        ).update({'priority': (Item.priority + 1) % 4})
        self.session.commit()

    def exists(self, chat_id: int, item: ItemData) -> bool:
        return self.session.query(Item.id).filter(
            Item.name == item.name,
            Item.chat_id == chat_id
        ).first() is not None


class FavouriteDAO:

    def __init__(self, session: Session) -> None:
        self.session = session

    def save(self, chat_id: int, item: ItemData) -> None:
        if not self.exists(chat_id, item):
            item_to_save = Favourite(
                chat_id=chat_id,
                name=item.name,
                url=item.url,
                priority=item.priority,
                checked=item.checked
            )
            self.session.add(item_to_save)
            self.session.commit()
        else:
            pass

    def get_all(self, chat_id: int) -> list[ItemData]:
        result = self.session.query(
            Favourite.name,
            Favourite.url,
            Favourite.priority,
            Favourite.checked,
        ).filter(
            Favourite.chat_id == chat_id
        ).all()

        return [ItemData(*item) for item in result]

    def delete_one(self, chat_id: int, item: ItemData) -> None:
        self.session.query(Favourite).filter(
            Favourite.name == item.name,
            Favourite.chat_id == chat_id
        ).delete()
        self.session.commit()

    def delete_checked(self, chat_id: int) -> None:
        self.session.query(Favourite).filter(
            Favourite.checked == True,
            Favourite.chat_id == chat_id,
        ).delete()
        self.session.commit()

    def delete_all(self, chat_id: int) -> None:
        self.session.query(Favourite).filter(
            Favourite.chat_id == chat_id
        ).delete()
        self.session.commit()

    def toggle_check(self, chat_id: int, item: ItemData) -> None:
        self.session.query(Favourite).filter(
            Favourite.name == item.name,
            Favourite.chat_id == chat_id
        ).update({'checked': not Favourite.checked})
        self.session.commit()

    def add_priority(self, chat_id: int, item: ItemData) -> None:
        self.session.query(Favourite).filter(
            Favourite.name == item.name,
            Favourite.chat_id == chat_id,
        ).update({'priority': (Favourite.priority + 1) % 4})
        self.session.commit()

    def exists(self, chat_id: int, item: ItemData) -> bool:
        return self.session.query(Favourite.id).filter(
            Favourite.name == item.name,
            Favourite.chat_id == chat_id
        ).first() is not None
