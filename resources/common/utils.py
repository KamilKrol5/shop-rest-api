import re
from typing import Dict, Any, Tuple, Optional, List

from flask import request
from flask_restful import Resource
from marshmallow import ValidationError

from db import ma, db


def add_to_allowed_methods(cls: Resource, method: str):
    if not cls.methods:
        cls.methods = set()
    cls.methods.add(method)


def handle_nonexistent_entry(entry_id, entry_name):
    return {"message": f"{entry_name} with id = {entry_id} does not exist."}, 404


def handle_no_json_body():
    return {"message": f"Invalid request. Request body must be valid JSON."}, 400


def _retrieve_kwarg_by_regex(regex, kwargs):
    for kwarg in kwargs:
        print(kwarg)
        if re.match(regex, kwarg):
            return kwarg, kwargs[kwarg]
    return None


def handle_request_validation_and_serialisation(
        schema_for_creation_obj: ma.SQLAlchemySchema
) -> Tuple[Dict[str, Any], Optional[int]]:
    if not request.is_json:
        return handle_no_json_body()
    try:
        item = schema_for_creation_obj.load(request.json, session=db.session)
    except ValidationError as err:
        return {"message": err.messages}, 400

    return item, None


def items_unique(elements: List[int]) -> bool:
    return len(elements) == len(set(elements))


def as_method(function):
    """Adds self argument to the function."""

    def new_func(self, *args, **kwargs):
        return function(*args, **kwargs)

    return new_func
