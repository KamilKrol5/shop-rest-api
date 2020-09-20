from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship

from db import db


class UserModel(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    email = Column(String, unique=True)
    orders = relationship('OrderModel', backref='users')
