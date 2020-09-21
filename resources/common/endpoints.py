import re
from typing import Type

from db import ma, db


def _retrieve_kwarg_by_regex(regex, kwargs):
    for kwarg in kwargs:
        print(kwarg)
        if re.match(regex, kwarg):
            return kwarg, kwargs[kwarg]
    return None


def _get_by_id(
        model_class: Type[db.Model],
        schema_obj: ma.SQLAlchemySchema,
        entry_id=None,
        **kwargs
):
    """
    Args:
        model_class (Type[SQLAlchemy.Model]):
            Model which is used to retrieve data. The class must support `find_by_id` function.
        schema_obj (Marshmallow.SQLAlchemySchema):
            Schema which is used to serialise the database entry.
        entry_id (int):
            The id of the element to get. If it is None, then entry id is searched in the kwargs.
            The keyword argument which has `id` in its name, is treated as entry_id.
    """
    if not entry_id:
        _, entry_id = _retrieve_kwarg_by_regex(r'.*id.*', kwargs)
        if not entry_id:
            return {'message': f'The arguments given to _find_by_id are invalid.'}, 500
    assert hasattr(model_class, 'find_by_id')
    entry = model_class.find_by_id(entry_id)
    if not entry:
        return {'message': f'Entry with id={entry_id} does not exist.'}, 404
    return schema_obj.dump(entry)


def _get_all(model_class: Type[db.Model], schema_obj: ma.SQLAlchemySchema):
    assert hasattr(model_class, 'find_all')
    entries = model_class.find_all()
    return schema_obj.dump(entries)
