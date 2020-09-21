import os

from flask import Flask
from flask_restful import Api

from app_cli_commands import db_cli
from model.item_category import ItemCategoryModel
from model.item import ItemModel
from model.user import UserModel
from model.order_element import OrderElementModel
from model.order_status import OrderStatus
from model.order import OrderModel

from db import db
from resources.items import Item, Items
from resources.users import User, Users

app = Flask(__name__)

base_directory = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(base_directory, "database.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # turns off flask_sqlalchemy modification tracker
# app.config['PROPAGATE_EXCEPTIONS'] = True

api = Api(app)
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(Users, '/users', '/users/all')
api.add_resource(Item, '/item/<int:item_id>')
api.add_resource(Items, '/items', '/items/all')

db.init_app(app)
app.cli.add_command(db_cli)

if __name__ == '__main__':
    db.init_app(app)
    app.run(debug=True)
