from db import ma
from model.order import OrderModel


class OrderSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = OrderModel
    # TODO: handle enum type


order_schema: ma.SQLAlchemyAutoSchema = OrderSchema()
orders_schema: ma.SQLAlchemyAutoSchema = OrderSchema(many=True)
