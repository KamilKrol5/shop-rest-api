from flask_restful import Resource

from model.item import ItemModel
from model.item_category import ItemCategoryModel
from model.schemas.item_category_schema import item_category_schema, item_categories_schema
from model.schemas.item_schema import item_schema, items_schema
from resources.common.decorators import add_get_all_endpoint, add_get_by_id_endpoint


@add_get_by_id_endpoint(ItemModel, item_schema)
class Item(Resource):
    pass


@add_get_all_endpoint(ItemModel, items_schema)
class Items(Resource):
    pass


@add_get_by_id_endpoint(ItemCategoryModel, item_category_schema)
class ItemCategory(Resource):
    pass


@add_get_all_endpoint(ItemCategoryModel, item_categories_schema)
class ItemCategories(Resource):
    pass
