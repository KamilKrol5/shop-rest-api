from db import ma


# def add_schema(cls):
#     class Schema(ma.Schema):
#         class Meta:
#             model = cls
#     cls.Schema = Schema
#     return cls


def create_basic_schema(cls) -> ma.SQLAlchemyAutoSchema:
    class Schema(ma.SQLAlchemyAutoSchema):
        class Meta:
            model = cls

    return Schema
