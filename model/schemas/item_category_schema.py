from model.item_category import ItemCategoryModel
from model.schemas.utils import create_basic_schema

ItemCategorySchema = create_basic_schema(ItemCategoryModel)

user_schema = ItemCategorySchema()
users_schema = ItemCategorySchema(many=True)
