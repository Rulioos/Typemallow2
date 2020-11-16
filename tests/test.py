from enum import Enum, auto

from marshmallow import Schema, fields
from marshmallow_enum import EnumField
from testfixtures import tempdir, compare

from typemallow2 import ts_interface, generate_ts, ts_enum
import unittest


def compare_files(output_lines, test_lines):
    '''
    Compares two files line by line. Return a boolean and a msg.
    Msg is empty if no error recorded.
    '''
    error = None
    is_equal = True
    for i in range(max(len(output_lines), len(test_lines))):
        if len(output_lines[i].strip()) < 1 or len(test_lines[i].strip()) < 1:
            break
        if output_lines[i].strip() != test_lines[i].strip():
            is_equal = False
            error = f'Error line {i}: \n Lines are not identical {output_lines[i]} != {test_lines[i]}'
            break

    return is_equal, error


class TestGenerateTsMethods(unittest.TestCase):

    @tempdir()
    def testComplexFile(self, dir):
        @ts_enum(value_is_auto=True)
        class MyAutoEnum(Enum):
            enum1 = auto()
            enum2 = auto()

        @ts_enum(value_is_auto=True)
        class MyNonAutoEnum(Enum):
            enum1 = 100
            enum2 = 200
            enum3 = "Baguette"

        @ts_enum(value_is_auto=False)
        class MyAutoEnumButValuesMatter(Enum):
            enum1 = auto()
            enum2 = auto()

        @ts_enum(value_is_auto=True)
        class MyNonAutoEnumWhereValuesAreNotImportant(Enum):
            enum1 = 100
            enum2 = 200
            enum3 = "Baguette"

        """ Interface tests """

        @ts_interface()
        class Bar(Schema):
            some_field = fields.Str()
            my_enum_field = EnumField(MyAutoEnum)

        @ts_interface()
        class Foo(Schema):
            some_field = fields.Str()
            another_field = fields.Str()
            my_field = fields.Bool()
            my_interface_field = fields.Nested(Bar, many=False)
            my_interfaces_fields = fields.Nested(Bar, many=True)

        generate_ts(dir.path + "/autoEnum.ts")
        with open("testFiles/complexTsFileTest.ts", 'r') as file:
            test_lines = file.readlines()

        with open(dir.path + "/autoEnum.ts", 'r') as file:
            output_lines = file.readlines()

        is_equal, error = compare_files(output_lines, test_lines)
        self.assertTrue(is_equal, msg=error)


if __name__ == '__main__':
    unittest.main()
