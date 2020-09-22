from typing import List, Optional, Dict

from flask_restful import Resource

from db import db
from model.item import ItemModel
from model.order import OrderModel
from model.order_element import OrderElementModel
from model.schemas.order_element_schema import order_element_schema, order_elements_schema, \
    order_element_creation_schema
from model.schemas.order_schema import order_schema, orders_schema, order_creation_schema
from model.user import UserModel
from resources.common.decorators import add_get_by_id_endpoint, add_get_all_endpoint
from resources.common.utils import handle_request_validation_and_serialisation, _items_unique


@add_get_by_id_endpoint(OrderElementModel, order_element_schema)
class OrderElement(Resource):
    pass


@add_get_all_endpoint(OrderElementModel, order_elements_schema)
class OrderElements(Resource):
    pass


@add_get_by_id_endpoint(OrderModel, order_schema)
class Order(Resource):
    pass


class CreateOrder(Resource):
    @staticmethod
    def post():
        result_dict, err_code = handle_request_validation_and_serialisation(order_creation_schema)
        if err_code:
            return result_dict, err_code

        if not result_dict['elements']:
            return {"message": "Cannot create an empty order. The order must have at least one element."}, 400

        elements = result_dict['elements']
        result_dict['elements'] = []
        order = OrderModel(**result_dict)

        if not UserModel.find_by_id(order.user_id):
            return {
                       "message": f"User with id: {order.user_id} does nor exist. "
                                  f"Cannot create an order for nonexistent user."
                   }, 400

        elements = [OrderElementModel(**order_element_creation_schema.load(e)) for e in elements]
        if err_msg := CreateOrder._validate_order_elements(elements):
            return err_msg, 400

        order.add_to_db()
        for elem in elements:
            elem.order_id = order.id
            elem.add_to_db()

        return {
                   "message": "Entry successfully created.",
                   "entry": order_schema.dump(order)
               }, 201

    @staticmethod
    def _validate_order_elements(elements: List[OrderElementModel]) -> Optional[Dict[str, str]]:
        """
        Validates order elements.

        Returns: dictionary with error message if validation fails, None otherwise.
        """
        if invalid := CreateOrder._validate_items_existence(elements):
            return {
                "message": "Some of order elements refer to nonexistent items. "
                           f"Item ids which does not exist: {','.join(map(str, invalid))}"
            }

        if not _items_unique([e.item_id for e in elements]):
            return {
                "message": "Order's elements contain 2 or more the same item_ids."
            }
        return None

    @staticmethod
    def _validate_items_existence(elements: List[OrderElementModel]) -> List[int]:
        """
        Validates the existence of item_id for every order element.

        Returns: List of nonexistent items.
        """
        invalid_elements = []
        with db.session.no_autoflush:
            for elem in elements:
                if not ItemModel.find_by_id(elem.item_id):
                    invalid_elements.append(elem.item_id)
        return invalid_elements


@add_get_all_endpoint(OrderModel, orders_schema)
class Orders(Resource):
    pass
