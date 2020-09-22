import os

from flask import Flask
from flask_restful import Api

from app_cli_commands import db_cli

from db import db
from resources.items import Item, Items, ItemCategory, ItemCategories, CreateItemCategory, CreateItem
from resources.orders import OrderElement, OrderElements, Orders, Order, CreateOrder
from resources.users import User, Users, UserCreation

app = Flask(__name__)

base_directory = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(base_directory, "database.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # turns off flask_sqlalchemy modification tracker
# app.config['PROPAGATE_EXCEPTIONS'] = True

api = Api(app)
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserCreation, '/user')
api.add_resource(Users, '/users', '/users/all')

api.add_resource(Item, '/item/<int:item_id>')
api.add_resource(CreateItem, '/item')
api.add_resource(Items, '/items', '/items/all')

api.add_resource(ItemCategory, '/item-category/<int:category_id>')
api.add_resource(CreateItemCategory, '/item-category')
api.add_resource(ItemCategories, '/item-categories', '/item-categories/all')

api.add_resource(OrderElement, '/order-element/<int:order_elem_id>')
api.add_resource(OrderElements, '/order-elements', '/order-elements/all')

api.add_resource(Order, '/order/<int:order_id>')
api.add_resource(CreateOrder, '/order')
api.add_resource(Orders, '/orders', '/orders/all')


db.init_app(app)
app.cli.add_command(db_cli)

if __name__ == '__main__':
    db.init_app(app)
    app.run(debug=True)
