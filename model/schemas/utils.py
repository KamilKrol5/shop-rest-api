from typing import Type

from db import ma


# def add_schema(cls):
#     class Schema(ma.Schema):
#         class Meta:
#             model = cls
#     cls.Schema = Schema
#     return cls


def create_basic_schema(cls, _include_relationships=False, _include_fk=False, excluded=()) -> Type[ma.SQLAlchemyAutoSchema]:
    class Schema(ma.SQLAlchemyAutoSchema):
        class Meta:
            model = cls
            include_relationships = _include_relationships
            include_fk = _include_fk
            exclude = excluded

    return Schema