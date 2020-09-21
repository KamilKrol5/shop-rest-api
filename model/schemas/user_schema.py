from marshmallow_sqlalchemy.fields import Nested

from db import ma
from model.schemas.order_schema import OrderSchemaRich
from model.schemas.utils import create_basic_schema
from model.user import UserModel

UserSchema = create_basic_schema(UserModel, _include_relationships=True)


class UserSchemaRich(UserSchema):
    orders = Nested(OrderSchemaRich, many=True)


user_schema: ma.SQLAlchemyAutoSchema = UserSchema()
user_schema_rich: ma.SQLAlchemyAutoSchema = UserSchemaRich()
users_schema: ma.SQLAlchemyAutoSchema = UserSchema(many=True)
