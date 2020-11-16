from enum import Enum, auto

from marshmallow import Schema, fields
from marshmallow_enum import EnumField

from typemallow2 import ts_enum, ts_interface, generate_ts


@ts_enum(value_is_auto=True)
class MyAutoEnum(Enum):
    enum1 = auto()
    enum2 = auto()


@ts_enum(value_is_auto=False)
class MyNonAutoEnum(Enum):
    enum1 = 100
    enum2 = 200
    enum3 = "Baguette"


@ts_interface()
class Boo(Schema):
    some_field = fields.Str()
    my_enum_field = EnumField(MyAutoEnum)


@ts_interface()
class Foo(Schema):
    some_field = fields.Str()
    another_field = fields.Str()
    my_field = fields.Bool()
    my_interface_field = fields.Nested(Boo, many=False)


generate_ts('./output.ts')
