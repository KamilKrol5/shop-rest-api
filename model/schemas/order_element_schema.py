from marshmallow_sqlalchemy.fields import Nested

from db import ma
from model.order_element import OrderElementModel
from model.schemas.item_schema import ItemSchemaRich
from model.schemas.utils import create_basic_schema

OrderElementSchema = create_basic_schema(OrderElementModel, _include_relationships=True)


class OrderElementSchemaRich(OrderElementSchema):
    item = Nested(ItemSchemaRich)


order_element_schema: ma.SQLAlchemyAutoSchema = OrderElementSchema()
order_element_schema_rich: ma.SQLAlchemyAutoSchema = OrderElementSchemaRich()
order_elements_schema: ma.SQLAlchemyAutoSchema = OrderElementSchema(many=True)
