from functools import partial
from typing import Type

from db import ma, db
from resources.common.endpoints import _get_by_id, _get_all


def add_get_by_id_endpoint(
        model_class: Type[db.Model],
        schema_obj: ma.SQLAlchemySchema
):
    def decorator(cls):
        setattr(cls, 'get', staticmethod(partial(_get_by_id, model_class, schema_obj)))
        return cls

    return decorator


def add_get_all_endpoint(
        model_class: Type[db.Model],
        schema_obj: ma.SQLAlchemySchema
):
    def decorator(cls):
        setattr(cls, 'get', staticmethod(partial(_get_all, model_class, schema_obj)))
        return cls

    return decorator
