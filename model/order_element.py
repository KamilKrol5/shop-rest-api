from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum, Table
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

from db import db
from model.order_status import OrderStatus


class OrderElementModel(db.Model):
    __tablename__ = 'order_elements'
    id = Column(Integer, primary_key=True)
    count = Column(Integer)
    order_id = Column(Integer, ForeignKey('orders.id'))
    item_id = Column(Integer, ForeignKey('items.id'))
