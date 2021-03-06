from flask_restful import Resource
from flask_restful_swagger_2 import swagger
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
    @swagger.doc({
        'description': 'Creates new item.',
        'responses': {
            '201': {
                'description': 'Item successfully created.'
            },
            '404': {
                'description': 'Provided item contains category id which does not exist.'
            },
            '400': {
                'description': 'Invalid data.'
            }
        },
        'tags': ['Adding new data']
    })
    def post(self):
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
                           }, 404
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


@add_post_basic_creation(ItemCategoryModel, item_category_creation_schema, item_category_schema)
class CreateItemCategory(Resource):
    pass


@add_get_all_endpoint(ItemCategoryModel, item_categories_schema)
class ItemCategories(Resource):
    pass
