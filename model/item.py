from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship

from db import db
from model.associations.item_and_item_category import item_category_and_item_association


class ItemModel(db.Model):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    price = Column(Float(precision=2))
    categories = relationship('ItemCategoryModel', secondary=item_category_and_item_association, back_populates='items')
