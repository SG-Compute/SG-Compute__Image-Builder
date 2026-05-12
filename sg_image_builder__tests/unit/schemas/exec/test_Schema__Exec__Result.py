from unittest import TestCase

from osbot_utils.testing.__ import __
from osbot_utils.type_safe.primitives.core.Safe_Int import Safe_Int
from osbot_utils.type_safe.primitives.core.Safe_UInt import Safe_UInt
from osbot_utils.type_safe.Type_Safe import Type_Safe

from sg_image_builder.schemas.exec.Schema__Exec__Result import Schema__Exec__Result
from sg_image_builder.types.safe_str.Safe_Str__Process__Text import Safe_Str__Process__Text


class test_Schema__Exec__Result(TestCase):
    def test__init__(self):  # Auto-init: every field has a sensible empty default
        with Schema__Exec__Result() as _:
            assert type(_) is Schema__Exec__Result
            assert isinstance(_, Type_Safe)
            assert _.obj() == __(command='', stdout='', stderr='', exit_code=0, elapsed_ms=0)

    def test__init__with_values(self):  # Auto-conversion of raw values to Safe_* types
        with Schema__Exec__Result(command='uname -a', stdout='Linux\n', stderr='', exit_code=0, elapsed_ms=142) as _:
            assert type(_.command) is Safe_Str__Process__Text
            assert type(_.stdout) is Safe_Str__Process__Text
            assert type(_.stderr) is Safe_Str__Process__Text
            assert type(_.exit_code) is Safe_Int
            assert type(_.elapsed_ms) is Safe_UInt
            assert _.obj() == __(command='uname -a', stdout='Linux\n', stderr='', exit_code=0, elapsed_ms=142)

    def test__preserves_stdout_whitespace(self):  # Regression: this is why we use Process__Text not Http__Text
        with Schema__Exec__Result(stdout='Linux ...\n') as _:
            assert str(_.stdout) == 'Linux ...\n'  # Trailing newline survives

    def test__preserves_command_shell_chars(self):  # Regression: this is why we use Process__Text not Safe_Str__Text
        with Schema__Exec__Result(command='/usr/bin/ls -la "x"') as _:
            assert str(_.command) == '/usr/bin/ls -la "x"'

    def test__accepts_negative_exit_code(self):  # Subprocess signal kill -> negative returncode on Unix
        with Schema__Exec__Result(exit_code=-130) as _:
            assert _.exit_code == -130

    def test__rejects_negative_elapsed_ms(self):  # Safe_UInt enforces >= 0
        with self.assertRaises(ValueError):
            Schema__Exec__Result(elapsed_ms=-1)

    def test__json_round_trip(self):  # Serialise + deserialise yields identical content
        with Schema__Exec__Result(command='echo hi', stdout='hi\n', exit_code=0, elapsed_ms=5) as original:
            restored = Schema__Exec__Result.from_json(original.json())
            assert restored.json() == original.json()
            assert type(restored.command) is Safe_Str__Process__Text
            assert type(restored.exit_code) is Safe_Int
            assert type(restored.elapsed_ms) is Safe_UInt
