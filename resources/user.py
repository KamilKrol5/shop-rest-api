from flask import jsonify
from flask_restful import Resource

from model.schemas.user_schema import user_schema
from model.user import UserModel


class User(Resource):
    @staticmethod
    def get(user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': f'User with id={user_id} does not exists.'}, 404
        return user_schema.dump(user), 200


