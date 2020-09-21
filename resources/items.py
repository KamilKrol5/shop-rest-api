from flask_restful import Resource

from model.item import ItemModel
from model.schemas.item_schema import item_schema, items_schema


class Item(Resource):
    @staticmethod
    def get(item_id):
        item = ItemModel.find_by_id(item_id)
        if not item:
            return {'message': f'Item with id={item_id} does not exists.'}, 404
        print(item.categories)
        return item_schema.dump(item)


class Items(Resource):
    @staticmethod
    def get():
        items = ItemModel.find_all()
        return items_schema.dump(items)
