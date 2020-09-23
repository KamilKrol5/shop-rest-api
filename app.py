import os

from flask import Flask
from flask_restful_swagger_2 import Api
from flask_swagger_ui import get_swaggerui_blueprint
from app_cli_commands import db_cli
from db import db
from resources.items.items import Item, Items, ItemCategory, ItemCategories, CreateItemCategory, CreateItem
from resources.orders.orders import OrderElement, OrderElements, Orders, Order, CreateOrder, UpdateOrderAdvanced
from resources.users.users import User, Users, UserCreation

app = Flask(__name__)

base_directory = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(base_directory, "database.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # turns off flask_sqlalchemy modification tracker

api = Api(app, api_version='0.0', api_spec_url='/api/swagger')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserCreation, '/user')
api.add_resource(Users, '/users')

api.add_resource(Item, '/item/<int:item_id>')
api.add_resource(CreateItem, '/item')
api.add_resource(Items, '/items')

api.add_resource(ItemCategory, '/item-category/<int:category_id>')
api.add_resource(CreateItemCategory, '/item-category')
api.add_resource(ItemCategories, '/item-categories')

api.add_resource(OrderElement, '/order-element/<int:order_elem_id>')
api.add_resource(OrderElements, '/order-elements')

api.add_resource(Order, '/order/<int:order_id>')
api.add_resource(CreateOrder, '/order')
api.add_resource(UpdateOrderAdvanced, '/order/advanced-update/<int:order_id>')
api.add_resource(Orders, '/orders')

db.init_app(app)

API_DOCS_URL = '/api/docs/ui'

docs_ui_blueprint = get_swaggerui_blueprint(API_DOCS_URL, "http://localhost:5000/api/swagger.json")

app.cli.add_command(db_cli)
app.register_blueprint(docs_ui_blueprint, url_prefix=API_DOCS_URL)

if __name__ == '__main__':
    db.init_app(app)
    app.run(debug=True)
