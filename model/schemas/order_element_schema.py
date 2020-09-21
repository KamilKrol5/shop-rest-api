from db import ma
from model.order_element import OrderElementModel
from model.schemas.utils import create_basic_schema

OrderElementSchema = create_basic_schema(OrderElementModel)

order_element_schema: ma.SQLAlchemyAutoSchema = OrderElementSchema()
order_elements_schema: ma.SQLAlchemyAutoSchema = OrderElementSchema(many=True)
