from db import ma
from model.schemas.utils import create_basic_schema
from model.user import UserModel

UserSchema = create_basic_schema(UserModel)

user_schema: ma.SQLAlchemyAutoSchema = UserSchema()
users_schema: ma.SQLAlchemyAutoSchema = UserSchema(many=True)
