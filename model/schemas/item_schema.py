from model.item import ItemModel
from model.schemas.utils import create_basic_schema

ItemSchema = create_basic_schema(ItemModel)

item_schema = ItemSchema()
items_schema = ItemSchema(many=True)
