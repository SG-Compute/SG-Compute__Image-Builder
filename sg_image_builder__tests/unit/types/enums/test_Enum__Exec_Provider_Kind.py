from enum import Enum
from unittest import TestCase

from sg_image_builder.types.enums.Enum__Exec_Provider_Kind import Enum__Exec_Provider_Kind


class test_Enum__Exec_Provider_Kind(TestCase):
    def test__values(self):  # Closed-set members + their string values
        assert Enum__Exec_Provider_Kind.LOCAL.value == 'local'
        assert Enum__Exec_Provider_Kind.SG_COMPUTE.value == 'sg_compute'

    def test__str_inheritance(self):  # Inherits str so it serialises cleanly
        assert isinstance(Enum__Exec_Provider_Kind.LOCAL, str)
        assert isinstance(Enum__Exec_Provider_Kind.LOCAL, Enum)

    def test____str__(self):  # __str__ returns the value, not the dotted name
        assert str(Enum__Exec_Provider_Kind.LOCAL) == 'local'
        assert str(Enum__Exec_Provider_Kind.SG_COMPUTE) == 'sg_compute'

    def test__construct_from_value(self):  # Roundtrip via value
        assert Enum__Exec_Provider_Kind('local') is Enum__Exec_Provider_Kind.LOCAL
        assert Enum__Exec_Provider_Kind('sg_compute') is Enum__Exec_Provider_Kind.SG_COMPUTE

    def test__construct__rejects_unknown(self):  # Closed set
        with self.assertRaises(ValueError):
            Enum__Exec_Provider_Kind('docker')

    def test__membership_is_exhaustive(self):  # Locks the set; expand only with care
        assert set(Enum__Exec_Provider_Kind) == {Enum__Exec_Provider_Kind.LOCAL, Enum__Exec_Provider_Kind.SG_COMPUTE}
