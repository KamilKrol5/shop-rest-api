from model.schemas.utils import create_basic_schema
from model.user import UserModel

UserSchema = create_basic_schema(UserModel)

user_schema = UserSchema()
users_schema = UserSchema(many=True)
