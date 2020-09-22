from typing import Type

from flask import request
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from db import ma, db
from resources.common.utils import _retrieve_kwarg_by_regex, handle_no_json_body


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


def _post(
        model_class: Type[db.Model],
        schema_for_creation_obj: ma.SQLAlchemySchema,
        schema_for_existing_obj: ma.SQLAlchemySchema,
        on_integrity_error_message=None
):
    assert hasattr(model_class, 'add_to_db')
    if not request.is_json:
        return handle_no_json_body()
    try:

        item = schema_for_creation_obj.load(request.json)
    except ValidationError as err:
        return {"message": err.messages}, 400

    item = model_class(**item)
    try:
        item.add_to_db()
    except IntegrityError:
        db.session.rollback()
        if not on_integrity_error_message:
            return {"message": f"Integrity error."}, 400
        return {"message": on_integrity_error_message}, 400

    return {
               "message": "Entry successfully created.",
               "entry": schema_for_existing_obj.dump(item)
           }, 201
