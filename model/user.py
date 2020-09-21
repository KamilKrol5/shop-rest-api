from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from db import db
from model.utils import create_basic_db_operations


@create_basic_db_operations
class UserModel(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    email = Column(String, unique=True)
    orders = relationship('OrderModel', backref='users')
