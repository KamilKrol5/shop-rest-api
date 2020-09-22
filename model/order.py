from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship

from db import db
from model.order_status import OrderStatus
from model.utils import create_basic_db_operations


@create_basic_db_operations
class OrderModel(db.Model):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    date = Column(DateTime, nullable=False, default=datetime.utcnow())
    comments = Column(String)
    status = Column(Enum(OrderStatus), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    elements = relationship("OrderElementModel", backref='order', cascade="all, delete-orphan")
