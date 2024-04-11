from sqlalchemy.orm import Session
from sqlalchemy import desc

from database.model import Item, Favourite
from database.item_data import ItemData

import logging


logging.basicConfig(
    level=logging.DEBUG,
    filename='log.log',
    format='%(asctime)s %(levelname)s %(message)s'
)


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

            logging.debug(f"{item} SAVED to Item table - save()")
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

        logging.debug(f"{result} SELECTED from Item table - get_all()")

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
                item=item
            )

            data.append(ItemData(
                item.name,
                item.url,
                item.priority,
                item.checked,
                is_in_fav
            ))

        logging.debug(f"{result} SELECTED from Item table - get_all_with_fav_data()")

        return data

    def delete_checked(self, chat_id: int) -> None:
        self.session.query(Item).filter(
            Item.checked == True,
            Item.chat_id == chat_id,
        ).delete()
        self.session.commit()

        logging.debug(f"CHECKED DELETED from Item table - delete_checked()")

    def delete_all(self, chat_id: int) -> None:
        self.session.query(Item).filter(
            Item.chat_id == chat_id
        ).delete()
        self.session.commit()

        logging.debug(f"ALL DELETED from Item table - delete_all()")

    def toggle_check(self, chat_id: int, item: ItemData) -> None:
        chckd = self.session.query(Item.checked).filter(
            Item.name == item.name,
            Item.chat_id == chat_id
        ).one()[0]

        logging.debug(f"{item} CHECK TOGGLE from {chckd} in Item table - toggle_check()")

        self.session.query(Item).filter(
            Item.name == item.name,
            Item.chat_id == chat_id
        ).update({'checked': not chckd})
        self.session.commit()
        

    def add_priority(self, chat_id: int, item: ItemData) -> None:
        self.session.query(Item).filter(
            Item.name == item.name,
            Item.chat_id == chat_id,
        ).update({'priority': (Item.priority + 1) % 4})
        self.session.commit()

        prrt = self.session.query(Item.priority).filter(
            Item.name == item.name,
            Item.chat_id == chat_id
        ).one()

        logging.debug(f"{item} PRIORITY ADDED to {prrt} in Item table - add_priority()")

    def exists(self, chat_id: int, item: ItemData) -> bool:
        exsts = self.session.query(Item.id).filter(
            Item.name == item.name,
            Item.chat_id == chat_id
        ).first() is not None

        logging.debug(f"{item} EXISTS={exsts} in Item table - exists()")

        return exsts


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

            logging.debug(f"{item} SAVED to Favourite table - save()")
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

        logging.debug(f"{result} SELECTED from Favourite table - get_all()")

        return [ItemData(*item) for item in result]

    def delete_one(self, chat_id: int, item: ItemData) -> None:
        self.session.query(Favourite).filter(
            Favourite.name == item.name,
            Favourite.chat_id == chat_id
        ).delete()
        self.session.commit()

        logging.debug(f"{item} DELETED from Favourite table - delete_one()")

    def delete_checked(self, chat_id: int) -> None:
        self.session.query(Favourite).filter(
            Favourite.checked == True,
            Favourite.chat_id == chat_id,
        ).delete()
        self.session.commit()

        logging.debug(f"CHECKED DELETED from Favourite table - delete_checked()")

    def delete_all(self, chat_id: int) -> None:
        self.session.query(Favourite).filter(
            Favourite.chat_id == chat_id
        ).delete()
        self.session.commit()

        logging.debug(f"ALL DELETED from Favourite table - delete_all()")

    def toggle_check(self, chat_id: int, item: ItemData) -> None:
        chckd = self.session.query(Favourite.checked).filter(
            Favourite.name == item.name,
            Favourite.chat_id == chat_id
        ).one()[0]

        logging.debug(f"{item} CHECK TOGGLE from {chckd} in Favourite table - toggle_check()")

        self.session.query(Favourite).filter(
            Favourite.name == item.name,
            Favourite.chat_id == chat_id
        ).update({'checked': not chckd})
        self.session.commit()
        

    def add_priority(self, chat_id: int, item: ItemData) -> None:
        self.session.query(Favourite).filter(
            Favourite.name == item.name,
            Favourite.chat_id == chat_id,
        ).update({'priority': (Favourite.priority + 1) % 4})
        self.session.commit()

        prrt = self.session.query(Favourite.priority).filter(
            Favourite.name == item.name,
            Favourite.chat_id == chat_id
        ).one()

        logging.debug(f"{item} PRIORITY ADDED to {prrt} in Favourite table - add_priority()")

    def exists(self, chat_id: int, item: ItemData) -> bool:
        exsts = self.session.query(Favourite.id).filter(
            Favourite.name == item.name,
            Favourite.chat_id == chat_id
        ).first() is not None

        logging.debug(f"{item} EXISTS = {exsts} in Favourite table - exists()")

        return exsts
