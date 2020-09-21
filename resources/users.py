from flask import jsonify
from flask_restful import Resource

from model.schemas.user_schema import user_schema, users_schema
from model.user import UserModel


# user registering, logging, etc.


class User(Resource):
    @staticmethod
    def get(user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': f'User with id={user_id} does not exists.'}, 404
        return user_schema.dump(user)


class Users(Resource):
    @staticmethod
    def get():
        users = UserModel.find_all()
        return users_schema.dump(users)
