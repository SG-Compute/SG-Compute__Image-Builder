from unittest import TestCase

from osbot_utils.testing.__ import __
from osbot_utils.type_safe.primitives.core.Safe_UInt import Safe_UInt
from osbot_utils.type_safe.primitives.domains.files.safe_str.Safe_Str__File__Path import (
    Safe_Str__File__Path,
)
from osbot_utils.type_safe.Type_Safe import Type_Safe

from sg_image_builder.schemas.exec.Schema__Exec__Request import Schema__Exec__Request
from sg_image_builder.types.safe_str.Safe_Str__Process__Text import Safe_Str__Process__Text


class test_Schema__Exec__Request(TestCase):
    def test__init__(self):  # Auto-init: empty command + empty env + 300s timeout
        with Schema__Exec__Request() as _:
            assert type(_) is Schema__Exec__Request
            assert isinstance(_, Type_Safe)
            assert _.obj() == __(command='', cwd=None, env=__(), timeout_seconds=300, user=None)

    def test__init__with_values(self):  # Field types after auto-conversion
        with Schema__Exec__Request(
            command='echo hi',
            cwd='/tmp',
            env={'FOO': 'bar'},
            timeout_seconds=60,
            user='ec2-user',
        ) as _:
            assert type(_.command) is Safe_Str__Process__Text
            assert type(_.cwd) is Safe_Str__File__Path
            assert type(_.timeout_seconds) is Safe_UInt
            assert type(_.user) is Safe_Str__Process__Text

    def test__preserves_shell_chars_in_command(self):  # Regression: raw Safe_Str would strip these
        with Schema__Exec__Request(command='/usr/bin/ls -la "with quotes"') as _:
            assert str(_.command) == '/usr/bin/ls -la "with quotes"'

    def test__preserves_path_with_colons_in_env(self):  # Env values commonly hold PATH-style colon lists
        with Schema__Exec__Request(env={'PATH': '/usr/bin:/bin:/usr/local/bin'}) as _:
            value = _.env[next(iter(_.env.keys()))]
            assert ':' in str(value)

    def test__rejects_negative_timeout(self):  # Safe_UInt enforces >= 0
        with self.assertRaises(ValueError):
            Schema__Exec__Request(timeout_seconds=-1)

    def test__json_round_trip(self):  # Serialise + deserialise preserves types
        with Schema__Exec__Request(
            command='whoami',
            cwd='/home/dev',
            timeout_seconds=10,
            user='root',
        ) as original:
            restored = Schema__Exec__Request.from_json(original.json())
            assert restored.json() == original.json()
            assert type(restored.command) is Safe_Str__Process__Text
            assert type(restored.timeout_seconds) is Safe_UInt
