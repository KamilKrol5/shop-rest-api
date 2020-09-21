def add_method(cls, method: str):
    if not cls.methods:
        cls.methods = set()
    cls.methods.add(method)


def handle_nonexistent_entry(entry_id, entry_name):
    return {"message": f"{entry_name} with id = {entry_id} does not exist."}, 404


def handle_no_json_body():
    return {"message": f"Invalid request. Request body must be valid JSON."}, 400
