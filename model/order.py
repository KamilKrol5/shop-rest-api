from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum, Table
from sqlalchemy.orm import relationship, backref

from db import db
from model.order_status import OrderStatus


class OrderModel(db.Model):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    comments = Column(String)
    status = Column(Enum(OrderStatus))
    user_id = Column(Integer, ForeignKey('users.id'))
    elements = relationship("OrderElementModel", backref='orders')
