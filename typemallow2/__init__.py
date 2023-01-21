from enum import Enum

from marshmallow import Schema, fields
from marshmallow_enum import EnumField

from .mappings import mappings

__schemas = {"default": []}
__enums = {"default": [], "auto": []}


def ts_enum(value_is_auto=False):
    '''

        Any valid Marshmallow schemas with this class decorator will
        be added to a list in a dictionary. An optional parameter: 'value_is_auto'
        may be provided, which will create separate dictionary keys per case.
        Otherwise, all values will be inserted into a list with a key of 'default'.

        e.g.

        @ts_interface(value_is_auto=True)
        class Foo(Enum):
            first_enum = 1

        '''

    def decorator(cls):
        if issubclass(cls, Enum):
            if value_is_auto:
                __enums["auto"].append(cls)
            else:
                __enums["default"].append(cls)
            return cls

    return decorator


def __get_ts_enum(enum, auto=True):
    '''

    Generates and returns a Typescript Enum by iterating
    through the declared Marshmallow fields of the Marshmallow Schema class
    passed in as a parameter, and mapping them to the appropriate Typescript
    data type.

    '''
    name = enum.__name__
    ts_fields = []
    if auto:
        for key in enum:
            ts_fields.append(
                f'\t{key.name}, '
            )
    else:
        for key in enum:
            if type(key.value) == str:
                ts_fields.append(
                    f'\t{key.name} = "{key.value}",'
                )
            else:
                ts_fields.append(
                    f'\t{key.name} = {key.value},'
                )

    ts_fields = '\n'.join(ts_fields)
    return f'export enum {name} {{\n{ts_fields}\n}}\n\n'


def ts_interface(context='default'):
    '''

    Any valid Marshmallow schemas with this class decorator will 
    be added to a list in a dictionary. An optional parameter: 'context'
    may be provided, which will create separate dictionary keys per context.
    Otherwise, all values will be inserted into a list with a key of 'default'.

    e.g.

    @ts_interface(context='internal')
    class Foo(Schema):
        first_field = fields.Integer()

    '''

    def decorator(cls):
        if issubclass(cls, Schema):
            if not context in __schemas:
                __schemas[context] = []
            __schemas[context].append(cls)
        return cls

    return decorator


def __get_ts_interface(schema):
    '''

    Generates and returns a Typescript Interface by iterating
    through the declared Marshmallow fields of the Marshmallow Schema class
    passed in as a parameter, and mapping them to the appropriate Typescript
    data type.

    '''
    name = schema.__name__.replace('Schema', '')
    ts_fields = []
    for key, value in schema._declared_fields.items():
        if type(value) is fields.Nested:
            if type(value.nested) is str:
                ts_type = value.nested.replace('Schema', '')
            else:
                ts_type = value.nested.__name__.replace('Schema', '')
            if value.many:
                ts_type += '[]'
        elif type(value) is EnumField:
            ts_type = value.enum.__name__
        else:
            ts_type = mappings.get(type(value), 'any')

        ts_fields.append(
            f'\t{key}: {ts_type};'
        )
    ts_fields = '\n'.join(ts_fields)
    return f'export interface {name} {{\n{ts_fields}\n}}\n\n'


def generate_ts(output_path, context='default'):
    '''

    When this function is called, a Typescript interface will be generated
    for each Marshmallow schema in the schemas dictionary, depending on the
    optional context parameter provided. If the parameter is ignored, all
    schemas in the default value, 'default' will be iterated over and a list
    of Typescript interfaces will be returned via a list comprehension.
    
    The Typescript interfaces will then be outputted to the file provided.

    '''
    with open(output_path, 'w') as output_file:
        interfaces = [__get_ts_interface(schema) for schema in __schemas[context]]
        enums_auto = [__get_ts_enum(enum) for enum in __enums["auto"]]
        enums_default = [__get_ts_enum(enum, False) for enum in __enums["default"]]
        output_file.write(''.join(enums_auto))
        output_file.write(''.join(enums_default))
        output_file.write(''.join(interfaces))



