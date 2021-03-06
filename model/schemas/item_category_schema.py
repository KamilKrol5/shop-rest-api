from db import ma
from model.item_category import ItemCategoryModel
from model.schemas.utils import create_basic_schema

ItemCategorySchema = create_basic_schema(ItemCategoryModel)
ItemCategoryCreationSchema = create_basic_schema(ItemCategoryModel, excluded=('id',))

item_category_schema: ma.SQLAlchemyAutoSchema = ItemCategorySchema()
item_category_creation_schema: ma.SQLAlchemyAutoSchema = ItemCategoryCreationSchema()
item_categories_schema: ma.SQLAlchemyAutoSchema = ItemCategorySchema(many=True)
