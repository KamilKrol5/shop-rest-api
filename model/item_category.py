from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from db import db
from model.associations.item_and_item_category import item_category_and_item_association
from model.utils import create_basic_db_operations


@create_basic_db_operations
class ItemCategoryModel(db.Model):
    __tablename__ = 'item_categories'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    items = relationship(
        "ItemModel",
        secondary=item_category_and_item_association,
        back_populates='categories'
    )
