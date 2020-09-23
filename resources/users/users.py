from flask import request
from flask_restful import Resource
from flask_restful_swagger_2 import swagger
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from db import db
from model.schemas.user_schema import user_schema, users_schema, user_creation_schema
from model.user import UserModel
from resources.common.decorators import add_get_by_id_endpoint, add_get_all_endpoint
from resources.common.utils import handle_no_json_body


# user registering, logging, etc.


@add_get_by_id_endpoint(UserModel, user_schema)
class User(Resource):
    pass


class UserCreation(Resource):
    @swagger.doc({
        'description': 'Creates new user.',
        'responses': {
            '201': {
                'description': 'User successfully created.'
            },
            '400': {
                'description': 'Invalid data or user with provided e-mail already exists.'
            }
        },
        'tags': ['Adding new data']
    })
    def post(self):
        if not request.is_json:
            return handle_no_json_body()
        try:
            item = user_creation_schema.load(request.json)
        except ValidationError as err:
            return {"message": err.messages}, 400

        item = UserModel(**item)
        try:
            item.add_to_db()
        except IntegrityError:
            db.session.rollback()
            return {"message": f"User with e-mail address: {item.email} already exists."}, 400

        return {"message": "Entry successfully created.", "entry": user_schema.dump(item)}, 201


@add_get_all_endpoint(UserModel, users_schema)
class Users(Resource):
    pass
