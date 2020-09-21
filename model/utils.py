from typing import Optional, Type, List

from db import db

T = Type[db.Model]


def find_by_id(model_class: T, _id) -> Optional[T]:
    return model_class.query.filter_by(id=_id).first()


def find_all(model_class: T) -> List[T]:
    return model_class.query.all()


def add_to_db(self):
    db.session.add(self)
    db.session.commit()


def add_all_to_db(items: List[T]):
    for item in items:
        item.add_to_db()


def update_in_db(self):
    self.add_to_db()


def update_all_in_db(items: List[T]):
    for item in items:
        item.update_in_db()


def delete_from_db(self):
    db.session.delete(self)
    db.session.commit()


def delete_all_from_db(items: List[T]):
    for item in items:
        item.delete_from_dc()


def create_basic_db_operations(cls):
    setattr(cls, find_by_id.__name__, classmethod(find_by_id))
    setattr(cls, find_all.__name__, classmethod(find_all))
    setattr(cls, add_to_db.__name__, add_to_db)
    setattr(cls, add_all_to_db.__name__, staticmethod(add_all_to_db))
    setattr(cls, update_in_db.__name__, update_in_db)
    setattr(cls, update_all_in_db.__name__, staticmethod(update_all_in_db))
    setattr(cls, delete_from_db.__name__, delete_from_db)
    setattr(cls, delete_all_from_db.__name__, staticmethod(delete_all_from_db))
    return cls
