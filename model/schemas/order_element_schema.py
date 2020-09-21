from model.order_element import OrderElementModel
from model.schemas.utils import create_basic_schema

OrderElementSchema = create_basic_schema(OrderElementModel)

user_schema = OrderElementSchema()
users_schema = OrderElementSchema(many=True)
