from marshmallow_sqlalchemy.fields import Nested

from db import ma
from model.item import ItemModel
from model.schemas.item_category_schema import ItemCategorySchema
from model.schemas.utils import create_basic_schema

ItemSchema = create_basic_schema(ItemModel, _include_relationships=True)
ItemCreationSchema = create_basic_schema(ItemModel, _include_relationships=True, excluded=('id',))


class ItemSchemaRich(ItemSchema):
    categories = Nested(ItemCategorySchema, many=True)


item_schema: ma.SQLAlchemyAutoSchema = ItemSchemaRich()
item_creation_schema: ma.SQLAlchemyAutoSchema = ItemCreationSchema()
items_schema: ma.SQLAlchemyAutoSchema = ItemSchema(many=True)
