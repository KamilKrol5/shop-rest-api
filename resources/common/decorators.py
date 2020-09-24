from functools import partial
from typing import Type

from flask_restful_swagger_2 import swagger

from db import ma, db
from resources.common.endpoints import _get_by_id, _get_all, _post, _delete
from resources.common.utils import add_to_allowed_methods, as_method


def add_get_by_id_endpoint(
        model_class: Type[db.Model],
        schema_obj: ma.SQLAlchemySchema
):
    def decorator(cls):
        get_method = as_method(partial(_get_by_id, model_class, schema_obj))
        get_method = swagger.doc({
            'description': 'Gets entry from the database by id provided in the path.',
            'parameters': [
                {
                    'name': 'entry_id',
                    'type': 'int',
                    'in': 'path'
                }
            ],
            'responses': {
                '200': {
                    'description': 'Entry successfully returned in the response body.'
                },
                '404': {
                    'description': 'Entry with provided id does not exists.'
                }
            },
            'tags': ['Getting data']
        })(get_method)
        setattr(cls, 'get', get_method)
        add_to_allowed_methods(cls, 'GET')
        return cls

    return decorator


def add_get_all_endpoint(
        model_class: Type[db.Model],
        schema_obj: ma.SQLAlchemySchema
):
    def decorator(cls):
        get_method = as_method(partial(_get_all, model_class, schema_obj))
        get_method = swagger.doc({
            'description': 'Gets all entries from the database.',
            'responses': {
                '200': {
                    'description': 'Entries successfully returned in the response body.'
                }
            },
            'tags': ['Getting data']
        })(get_method)
        setattr(cls, 'get', get_method)
        add_to_allowed_methods(cls, 'GET')
        return cls

    return decorator


def add_post_basic_creation(
        model_class: Type[db.Model],
        schema_for_creation_obj: ma.SQLAlchemySchema,
        schema_for_existing_obj: ma.SQLAlchemySchema
):
    def decorator(cls):
        post_method = as_method(
            partial(
                _post,
                model_class,
                schema_for_creation_obj,
                schema_for_existing_obj
            )
        )
        post_method = swagger.doc({
            'description': 'Adds an entry specified in the request body to the database.',
            'responses': {
                '201': {
                    'description': 'Entry successfully added.'
                },
                '400': {
                    'description': 'Invalid entry in the request body '
                                   'or provided entry is violating the database integrity.'
                }
            },
            'tags': ['Adding new data']
        })(post_method)
        setattr(cls, 'post', post_method)
        add_to_allowed_methods(cls, 'POST')
        return cls

    return decorator


def add_delete_endpoint(model_class: Type[db.Model]):
    def decorator(cls):
        method = swagger.doc({
            'description': 'Deletes an entry with given id.',
            'parameters': [
                {
                    'name': 'entry_id',
                    'type': 'int',
                    'in': 'path'
                }
            ],
            'responses': {
                '200': {
                    'description': 'Entry successfully deleted.'
                },
                '404': {
                    'description': 'An attempt to delete non-existing entry.'
                }
            },
            'tags': ['Deleting data']
        })(as_method(partial(_delete, model_class)))
        setattr(cls, 'delete', method)
        add_to_allowed_methods(cls, 'DELETE')
        return cls

    return decorator
