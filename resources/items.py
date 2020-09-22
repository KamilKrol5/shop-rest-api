from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

from db import db
from model.item import ItemModel
from model.item_category import ItemCategoryModel
from model.schemas.item_category_schema import item_category_creation_schema, item_category_schema, \
    item_categories_schema
from model.schemas.item_schema import item_schema, items_schema, item_creation_schema
from resources.common.decorators import add_get_all_endpoint, add_get_by_id_endpoint, add_post_basic_creation
from resources.common.utils import handle_request_validation_and_serialisation


@add_get_by_id_endpoint(ItemModel, item_schema)
class Item(Resource):
    pass


@add_get_all_endpoint(ItemModel, items_schema)
class Items(Resource):
    pass


class CreateItem(Resource):
    @staticmethod
    def post():
        result_dict, err_code = handle_request_validation_and_serialisation(item_creation_schema)
        if err_code:
            return result_dict, err_code
        with db.session.no_autoflush:
            item = ItemModel(**result_dict)
            if not item.categories:
                return {"message": f'Item must have at lest one category.'}, 400
            for cat in item.categories:
                c_id = cat.id
                if not ItemCategoryModel.find_by_id(c_id):
                    return {
                               "message": f"Category with id: {c_id} does not exists. "
                                          f"Item's category id's must exist before the item can be created. "
                                          f"Create this category and try again."
                           }, 400
        try:
            item.add_to_db()
        except IntegrityError:
            return {"message": "An integrity error has occurred while adding to the database."}, 400
        return {
                   "message": "Entry successfully created.",
                   "entry": item_schema.dump(item)
               }, 201


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


@add_post_basic_creation(ItemCategoryModel, item_category_creation_schema, item_category_schema)
class CreateItemCategory(Resource):
    pass


@add_get_all_endpoint(ItemCategoryModel, item_categories_schema)
class ItemCategories(Resource):
    pass
