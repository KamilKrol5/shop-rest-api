import re

from flask_restful import Resource


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
