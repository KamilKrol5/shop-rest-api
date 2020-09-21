from flask_restful import Resource

from model.order import OrderModel
from model.order_element import OrderElementModel
from model.schemas.order_element_schema import order_element_schema, order_elements_schema
from model.schemas.order_schema import order_schema, orders_schema
from resources.common.decorators import add_get_by_id_endpoint, add_get_all_endpoint


@add_get_by_id_endpoint(OrderElementModel, order_element_schema)
class OrderElement(Resource):
    pass


@add_get_all_endpoint(OrderElementModel, order_elements_schema)
class OrderElements(Resource):
    pass


@add_get_by_id_endpoint(OrderModel, order_schema)
class Order(Resource):
    pass


@add_get_all_endpoint(OrderModel, orders_schema)
class Orders(Resource):
    pass
