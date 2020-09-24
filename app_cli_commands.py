from flask.cli import AppGroup

from db import db
from model.item import ItemModel
from model.item_category import ItemCategoryModel
from model.order import OrderModel
from model.order_element import OrderElementModel
from model.order_status import OrderStatus
from model.user import UserModel

db_cli = AppGroup('db', '')


@db_cli.command('db_create')
def db_create():
    db.create_all()


@db_cli.command('db_populate')
def db_populate():
    users = [
        UserModel(id=1, name='Karol Krawczyk', email='karol_krawczyk@gmail.com'),
        UserModel(id=2, name='Monica Geller', email='geller_mon@gmail.com'),
        UserModel(id=3, name='Rachel Green', email='rachel_g@gmail.com'),
        UserModel(id=4, name='Paweł Okrutnik', email='pawel7312@gmail.com'),
        UserModel(id=5, name='Danuta Norek', email='tadziknagore@gmail.com'),
    ]
    categories = [
        ItemCategoryModel(name='fun'),
        ItemCategoryModel(name='antique'),
        ItemCategoryModel(name='music'),
        ItemCategoryModel(name='computer'),
    ]
    items = [
        ItemModel(id=1, name='Good Processor', price=199.9, categories=[
            categories[0], categories[3]
        ]),
        ItemModel(id=2, name='Komputer 100 Giga', price=2499.99, categories=[
            categories[0], categories[3]
        ]),
        ItemModel(id=3, name='Wiadro firmy WiadroPOL', price=120, categories=[
            categories[1]
        ]),
        ItemModel(id=4, name='Fleetwood Mac - Tango In The Night, vinyl', price=26.99, categories=[
            categories[2]
        ]),
        ItemModel(id=5, name='Keyboard 3000', price=549.99, categories=[
            categories[0], categories[2]
        ]),
    ]
    orders = [
        OrderModel(id=1, status=OrderStatus.awaiting_payment, user_id=2, elements=[
            OrderElementModel(id=1, count=4, order_id=1, item_id=1),
            OrderElementModel(id=2, count=10, order_id=1, item_id=3)
        ]),
        OrderModel(id=2, status=OrderStatus.delivered, user_id=4, elements=[
            OrderElementModel(id=3, count=2, order_id=2, item_id=5),
            OrderElementModel(id=4, count=1, order_id=2, item_id=4),
            OrderElementModel(id=5, count=1, order_id=2, item_id=2),
        ])
    ]
    for user in users:
        db.session.add(user)
    for category in categories:
        db.session.add(category)
    for item in items:
        db.session.add(item)
    for order in orders:
        db.session.add(order)
    db.session.commit()


@db_cli.command('db_delete')
def db_delete():
    db.drop_all()
