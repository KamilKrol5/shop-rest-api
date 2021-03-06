from typing import Type

from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from db import ma


def create_basic_schema(
        cls,
        _include_relationships=False,
        _include_fk=False,
        excluded=()
) -> Type[ma.SQLAlchemyAutoSchema]:
    class Schema(SQLAlchemyAutoSchema):
        class Meta:
            model = cls
            include_relationships = _include_relationships
            include_fk = _include_fk
            exclude = excluded

    return Schema
