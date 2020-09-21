from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from db import db
from model.utils import create_basic_db_operations


@create_basic_db_operations
class OrderElementModel(db.Model):
    __tablename__ = 'order_elements'
    id = Column(Integer, primary_key=True)
    count = Column(Integer, nullable=False, default=1)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    item_id = Column(Integer, ForeignKey('items.id'), nullable=False)
    item = relationship("ItemModel")
