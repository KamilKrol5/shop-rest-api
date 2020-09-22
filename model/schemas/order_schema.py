from marshmallow_sqlalchemy.fields import Nested

from db import ma
from model.order import OrderModel
from model.schemas.order_element_schema import OrderElementSchemaRich, OrderElementCreationSchema
from model.schemas.utils import create_basic_schema

OrderSchema = create_basic_schema(OrderModel, _include_relationships=True)
_OrderCreationSchema = create_basic_schema(
    OrderModel,
    _include_fk=True,
    _include_relationships=True,
    excluded=('id', 'date', 'user')
)
OrderUpdateSchema = create_basic_schema(
    OrderModel,
    _include_fk=True,
    excluded=('id', 'date', 'user')
)


class OrderCreationSchema(_OrderCreationSchema):
    elements = Nested(OrderElementCreationSchema, many=True, exclude=('order_id',))


class OrderSchemaRich(OrderSchema):
    elements = Nested(OrderElementSchemaRich, many=True, exclude=('order',))


order_schema: ma.SQLAlchemyAutoSchema = OrderSchemaRich()
order_creation_schema: ma.SQLAlchemyAutoSchema = OrderCreationSchema()
order_update_schema: ma.SQLAlchemyAutoSchema = OrderUpdateSchema()
orders_schema: ma.SQLAlchemyAutoSchema = OrderSchema(many=True)
orders_schema_rich: ma.SQLAlchemyAutoSchema = OrderSchemaRich(many=True)
