from marshmallow_sqlalchemy.fields import Nested

from db import ma
from model.order import OrderModel
from model.schemas.order_element_schema import OrderElementSchemaRich
from model.schemas.utils import create_basic_schema

OrderSchema = create_basic_schema(OrderModel, _include_relationships=True)


class OrderSchemaRich(OrderSchema):
    elements = Nested(OrderElementSchemaRich, many=True, exclude=('order',))


order_schema: ma.SQLAlchemyAutoSchema = OrderSchemaRich()
orders_schema: ma.SQLAlchemyAutoSchema = OrderSchema(many=True)
orders_schema_rich: ma.SQLAlchemyAutoSchema = OrderSchemaRich(many=True)
