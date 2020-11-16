# typemallow 2
_An elegant and automatic solution for generating/outputting Typescript interfaces from your Marshmallow Schemas_

 
I updated the typemallow package so it could Handle enums in typescript and more recent versions of marshmallow.
Original work is from adenh93.
### Usage:

_Using typemallow2 is simple._

First, install the package 
`pip install typemallow2`

Next, for your Marshmallow schemas that you wish to generate Typescript interfaces for, simply import `ts_interface` and `generate_ts` from the `typemallow` module, and prepend the `@ts_interface()` class decorator to your Marshmallow schema class.

All that is required to generate your Typescript interfaces is to call the `generate_ts()` function, and provide a filepath as a parameter to output the result.

_main.py_
```python
from typemallow2 import ts_interface, generate_ts


@ts_interface()
class Foo(Schema):
    some_field = fields.Str()
    another_field = fields.Date()


generate_ts('./output.ts')
```

_output.ts_
```typescript
export interface Foo {
    some_field: string;
    another_field: date;
}
```

_typemallow_ even supports Nested Schema fields and enums.

_main.py_
```python
from typemallow2 import ts_interface, generate_ts, ts_enum
from marshmallow import Schema, fields
from marshmallow_enum import EnumField
from enum import Enum, auto


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
```
_output.ts_
```typescript

export enum MyAutoEnum {
	enum1,
	enum2,
}

export interface Bar {
	some_field: string;
	my_enum_field: MyAutoEnum;
}

export interface Foo {
	some_field: string;
	another_field: string;
	my_field: boolean;
	my_interface_field: Bar;
	my_interfaces_fields: Bar[];
}

```

### Extended Usage:
The `@ts_interface()` decorator function accepts an optional parameter, _context_, which defaults to... well... 'default'.

"_Why is this the case?_" 

When a Marshmallow Schema is identified with with `@ts_interface` decorator, it is added to a list in a dictionary of schemas, with the dictionary key being the value provided to the _context_ parameter. If you were to provide different contexts for each schema, additional keys will be created if they do not exist, or the schema will simply be appended to the list at the existing key.

This comes in handy, as the `generate_ts()` function _also_ accepts an optional _context_ parameter, which will filter only schemas in the dictionary at the specific key.

This is useful if you wish to output different contexts to different files, e.g.

_main.py_
```python
...
from typemallow2 import ts_interface, generate_ts

@ts_interface(context='internal')
class Foo(Schema):
    foo = fields.Str()


@ts_interface(context='internal')
class Bar(Schema):
    bar = fields.Str()
 

@ts_interface(context='external')
class FooBar(Schema):
    foo_bar = fields.Str()


''' 
we're telling typemallow2 that we only want to generate interfaces from Schemas with 
an 'internal' context to './internal.ts' 
'''
generate_ts('./internal.ts', context='internal')

''' 
only generate interfaces from Schemas with an 'external' context to './external.ts' 
'''
generate_ts('./external.ts', context='external')
```

_internal.ts_
```typescript
export interface Foo {
    foo: string;
}

export interface Bar {
    bar: string;
}
```

_external.ts_
```typescript
export interface FooBar {
    foo_bar: string;
}
```

