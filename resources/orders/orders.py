from flask_restful import Resource
from flask_restful_swagger_2 import swagger

from model.order import OrderModel
from model.order_element import OrderElementModel
from model.schemas.order_element_schema import order_element_schema, order_elements_schema, \
    order_element_creation_schema
from model.schemas.order_schema import order_schema, orders_schema, order_creation_schema, order_update_schema
from model.user import UserModel
from resources.common.decorators import add_get_by_id_endpoint, add_get_all_endpoint, add_delete_endpoint
from resources.common.utils import handle_request_validation_and_serialisation
from resources.orders.utils import _validate_order_elements


@add_get_by_id_endpoint(OrderElementModel, order_element_schema)
class OrderElement(Resource):
    pass


@add_get_all_endpoint(OrderElementModel, order_elements_schema)
class OrderElements(Resource):
    pass


@add_get_by_id_endpoint(OrderModel, order_schema)
@add_delete_endpoint(OrderModel)
class Order(Resource):
    @swagger.doc({
        'description': 'Updates an order. So as to cange order elements use '
                       '`/order/advanced-update/{order_id} endpoint.',
        'responses': {
            '200': {
                'description': 'Order successfully updated.'
            },
            '400': {
                'description': 'Invalid input.'
            }
        },
        'tags': ['Updating data']
    })
    def put(self, order_id: int):
        result_dict, err_code = handle_request_validation_and_serialisation(order_update_schema)
        if err_code:
            return result_dict, err_code

        order = OrderModel.find_by_id(order_id)
        if not order:
            return {"message": f"Order with id: {order_id} does not exist."}, 400

        order.user_id = result_dict.get('user_id', order.user_id)
        order.status = result_dict.get('status', order.status)
        order.comments = result_dict.get('comments', order.comments)
        order.update_in_db()

        return {"message": f"The order with id: {order.id} updated successfully.",
                "entry": order_schema.dump(order)}, 200


class UpdateOrderAdvanced(Resource):
    @swagger.doc({
        'description': 'Updates an order. The order can be fully edited, including its items.',
        'parameters': [
            {
                'name': 'order_id',
                'type': 'int',
                'in': 'path'
            }
        ],
        'responses': {
            '200': {
                'description': 'Order successfully updated.'
            },
            '404': {
                'description': 'Order with provided id does nor exist.'
            },
            '400': {
                'description': 'Invalid input.'
            }
        },
        'tags': ['Updating data']
    })
    def put(self, order_id: int):
        result_dict, err_code = handle_request_validation_and_serialisation(order_creation_schema)
        if err_code:
            return result_dict, err_code

        if not result_dict['elements']:
            return {"message": "The order cannot be empty. The order must have at least one element."}, 400

        order = OrderModel.find_by_id(order_id)
        if not order:
            return {"message": f"Order with id: {order_id} does not exist."}, 404

        new_elements = result_dict['elements']
        old_elements = [order_element_creation_schema.dump(e) for e in order.elements]

        old_to_delete = [e['item_id'] for e in old_elements if e not in new_elements]
        new_to_add = [e for e in new_elements if e not in old_elements]
        # useful for debugging purposes
        # print('O', old_elements)
        # print('N', new_elements)
        # print(old_to_delete)
        # print(new_to_add)

        # for x in order.elements:
        #     print(x.item_id in old_to_delete)

        old_to_delete = list(filter(lambda x: x.item_id in old_to_delete, order.elements))
        OrderElementModel.delete_all_from_db(old_to_delete)

        new_to_add = [OrderElementModel(**order_element_creation_schema.load(e)) for e in new_to_add]
        if err_msg := _validate_order_elements(new_to_add):
            return err_msg, 400

        for n_elem in new_to_add:
            n_elem.order_id = order.id

        order.user_id = result_dict['user_id']
        order.status = result_dict['status']
        order.comments = result_dict['comments']
        order.elements = order.elements + new_to_add

        order.update_in_db()

        return {"message": f"The order with id: {order.id} updated successfully.",
                "entry": order_schema.dump(order)}, 200


class CreateOrder(Resource):
    @swagger.doc({
        'description': 'Creates an order.',
        'responses': {
            '201': {
                'description': 'Order successfully created.'
            },
            '400': {
                'description': 'Invalid input.'
            }
        },
        'tags': ['Adding new data']
    })
    def post(self):
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
        if err_msg := _validate_order_elements(elements):
            return err_msg, 400

        order.add_to_db()
        for elem in elements:
            elem.order_id = order.id
            elem.add_to_db()

        return {
                   "message": "Entry successfully created.",
                   "entry": order_schema.dump(order)
               }, 201


@add_get_all_endpoint(OrderModel, orders_schema)
class Orders(Resource):
    pass
