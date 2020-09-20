from sqlalchemy import Column, Integer, ForeignKey, Table

from db import db

item_category_and_item_association = Table(
    "item_category_and_item_association",
    db.Model.metadata,
    Column('item_id', Integer, ForeignKey('items.id'), primary_key=True),
    Column('item_category_id', Integer, ForeignKey('item_categories.id'), primary_key=True))
