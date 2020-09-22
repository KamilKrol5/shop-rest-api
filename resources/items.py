from flask import request
from flask_restful import Resource
from marshmallow import ValidationError

from model.item import ItemModel
from model.item_category import ItemCategoryModel
from model.schemas.item_category_schema import item_category_creation_schema, item_category_schema, \
    item_categories_schema
from model.schemas.item_schema import item_schema, items_schema
from resources.common.decorators import add_get_all_endpoint, add_get_by_id_endpoint
from resources.common.utils import handle_no_json_body


@add_get_by_id_endpoint(ItemModel, item_schema)
class Item(Resource):
    pass


@add_get_all_endpoint(ItemModel, items_schema)
class Items(Resource):
    pass


@add_get_by_id_endpoint(ItemCategoryModel, item_category_schema)
class ItemCategory(Resource):
    pass
    # @staticmethod
    # def put(category_id=None):
    #     if not request.is_json:
    #         return {"message": f"Invalid request. Request body must be valid JSON."}, 400
    #     print(request.json)
    #     item = item_category_schema.load(request.json)
    #     print(item)
    #     print(ItemCategory.__dict__)
    #
    #     return {}, 201


class CreateItemCategory(Resource):
    @staticmethod
    def post():
        if not request.is_json:
            return handle_no_json_body()
        try:
            item = item_category_creation_schema.load(request.json)
        except ValidationError as err:
            return {"message": err.messages}, 400

        item = ItemCategoryModel(**item)
        item.add_to_db()


@add_get_all_endpoint(ItemCategoryModel, item_categories_schema)
class ItemCategories(Resource):
    pass
