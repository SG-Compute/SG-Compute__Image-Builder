from enum import Enum
from unittest import TestCase

from sg_image_builder.types.enums.Enum__Exit_Code import Enum__Exit_Code


class test_Enum__Exit_Code(TestCase):
    def test__values(self):  # Numeric values match POSIX / Typer convention
        assert Enum__Exit_Code.SUCCESS.value == 0
        assert Enum__Exit_Code.GENERIC_ERROR.value == 1
        assert Enum__Exit_Code.CLI_USAGE_ERROR.value == 2
        assert Enum__Exit_Code.INTERRUPTED.value == 130  # SIGINT exit code

    def test__int_inheritance(self):  # Inherits int so it works in subprocess returncode comparisons
        assert isinstance(Enum__Exit_Code.SUCCESS, int)
        assert isinstance(Enum__Exit_Code.SUCCESS, Enum)
        assert Enum__Exit_Code.SUCCESS == 0
        assert Enum__Exit_Code.GENERIC_ERROR != 0

    def test____str__(self):  # __str__ returns the numeric string (sys.exit-friendly)
        assert str(Enum__Exit_Code.SUCCESS) == '0'
        assert str(Enum__Exit_Code.GENERIC_ERROR) == '1'
        assert str(Enum__Exit_Code.CLI_USAGE_ERROR) == '2'
        assert str(Enum__Exit_Code.INTERRUPTED) == '130'

    def test__construct_from_value(self):  # Round-trip via int value
        assert Enum__Exit_Code(0) is Enum__Exit_Code.SUCCESS
        assert Enum__Exit_Code(1) is Enum__Exit_Code.GENERIC_ERROR
        assert Enum__Exit_Code(130) is Enum__Exit_Code.INTERRUPTED

    def test__construct__rejects_unknown(self):  # Closed set: 99 isn't defined yet
        with self.assertRaises(ValueError):
            Enum__Exit_Code(99)

    def test__membership_is_exhaustive(self):  # Locks the set; extend deliberately
        assert set(Enum__Exit_Code) == {
            Enum__Exit_Code.SUCCESS,
            Enum__Exit_Code.GENERIC_ERROR,
            Enum__Exit_Code.CLI_USAGE_ERROR,
            Enum__Exit_Code.INTERRUPTED,
        }
