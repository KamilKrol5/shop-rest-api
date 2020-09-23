from typing import Type, Optional

from sqlalchemy.exc import IntegrityError

from db import ma, db
from resources.common.utils import _retrieve_kwarg_by_regex, handle_request_validation_and_serialisation


def _get_by_id(
        model_class: Type[db.Model],
        schema_obj: ma.SQLAlchemySchema,
        entry_id: Optional[int] = None,
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
    result_dict, err_code = handle_request_validation_and_serialisation(schema_for_creation_obj)
    if err_code:
        return result_dict, err_code
    item = model_class(**result_dict)
    try:
        item.add_to_db()
    except IntegrityError:
        if not on_integrity_error_message:
            return {"message": f"Integrity error."}, 400
        return {"message": on_integrity_error_message}, 400

    return {
               "message": "Entry successfully created.",
               "entry": schema_for_existing_obj.dump(item)
           }, 201


def _delete(
        model_class: Type[db.Model],
        entry_id: Optional[int] = None,
        **kwargs
):
    """
    Args:
        model_class (Type[SQLAlchemy.Model]):
            Model which is used to reach the database. The class must support `delete_from_db` function.
        entry_id (int):
            The id of the element to delete. If it is None, then entry id is searched in the kwargs.
            The keyword argument which has `id` in its name, is treated as entry_id.
    """
    if not entry_id:
        _, entry_id = _retrieve_kwarg_by_regex(r'.*id.*', kwargs)
        if not entry_id:
            return {'message': f'The arguments given to _find_by_id are invalid.'}, 500

    assert hasattr(model_class, 'delete_from_db')

    entry = model_class.find_by_id(entry_id)
    if not entry:
        return {"message": f"The entry with id: {entry_id} does not exist."}, 404
    entry.delete_from_db()

    return {"message": f"The entry with id: {entry_id} was successfully deleted."}, 200
