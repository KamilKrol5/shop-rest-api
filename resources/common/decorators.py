from functools import partial
from typing import Type

from db import ma, db
from resources.common.endpoints import _get_by_id, _get_all, _post, _delete
from resources.common.utils import add_to_allowed_methods


def add_get_by_id_endpoint(
        model_class: Type[db.Model],
        schema_obj: ma.SQLAlchemySchema
):
    def decorator(cls):
        setattr(cls, 'get', staticmethod(partial(_get_by_id, model_class, schema_obj)))
        add_to_allowed_methods(cls, 'GET')
        return cls

    return decorator


def add_get_all_endpoint(
        model_class: Type[db.Model],
        schema_obj: ma.SQLAlchemySchema
):
    def decorator(cls):
        setattr(cls, 'get', staticmethod(partial(_get_all, model_class, schema_obj)))
        add_to_allowed_methods(cls, 'GET')
        return cls

    return decorator


def add_post_basic_creation(
        model_class: Type[db.Model],
        schema_for_creation_obj: ma.SQLAlchemySchema,
        schema_for_existing_obj: ma.SQLAlchemySchema
):
    def decorator(cls):
        post_method = staticmethod(
            partial(
                _post,
                model_class,
                schema_for_creation_obj,
                schema_for_existing_obj
            )
        )
        setattr(cls, 'post', post_method)
        add_to_allowed_methods(cls, 'POST')
        return cls

    return decorator


def add_delete_endpoint(model_class: Type[db.Model]):
    def decorator(cls):
        setattr(cls, 'delete', staticmethod(partial(_delete, model_class)))
        add_to_allowed_methods(cls, 'DELETE')
        return cls

    return decorator
