from flask_restful import Resource

from model.schemas.user_schema import user_schema, users_schema
from model.user import UserModel
from resources.common.decorators import add_get_by_id_endpoint, add_get_all_endpoint


# user registering, logging, etc.


@add_get_by_id_endpoint(UserModel, user_schema)
class User(Resource):
    pass


@add_get_all_endpoint(UserModel, users_schema)
class Users(Resource):
    pass
