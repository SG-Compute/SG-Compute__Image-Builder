from unittest import TestCase

from osbot_utils.testing.__ import __
from osbot_utils.type_safe.primitives.domains.files.safe_str.Safe_Str__File__Path import (
    Safe_Str__File__Path,
)
from osbot_utils.type_safe.Type_Safe import Type_Safe

from sg_image_builder.schemas.exec.Schema__Exec__File__Transfer import (
    Schema__Exec__File__Transfer,
)
from sg_image_builder.types.safe_str.Safe_Str__Process__Text import Safe_Str__Process__Text


class test_Schema__Exec__File__Transfer(TestCase):
    def test__init__(self):  # Auto-init: paths empty, mode and owner None
        with Schema__Exec__File__Transfer() as _:
            assert type(_) is Schema__Exec__File__Transfer
            assert isinstance(_, Type_Safe)
            assert _.obj() == __(local_path='', remote_path='', mode=None, owner=None)

    def test__init__with_values(self):  # Auto-conversion of raw strings to Safe_* types
        with Schema__Exec__File__Transfer(
            local_path='/tmp/x',
            remote_path='/opt/x',
            mode='a+x',
            owner='ec2-user:ec2-user',
        ) as _:
            assert type(_.local_path) is Safe_Str__File__Path
            assert type(_.remote_path) is Safe_Str__File__Path
            assert type(_.mode) is Safe_Str__Process__Text
            assert type(_.owner) is Safe_Str__Process__Text

    def test__preserves_owner_colon(self):  # chown spec 'user:group' has a `:` - must survive
        with Schema__Exec__File__Transfer(owner='ec2-user:ec2-user') as _:
            assert str(_.owner) == 'ec2-user:ec2-user'

    def test__preserves_mode_plus(self):  # chmod mode 'a+x' has a `+` - must survive
        with Schema__Exec__File__Transfer(mode='a+x') as _:
            assert str(_.mode) == 'a+x'

    def test__json_round_trip(self):  # Serialise + deserialise preserves types
        with Schema__Exec__File__Transfer(
            local_path='/tmp/bundle.zst',
            remote_path='/opt/bundle.zst',
            mode='0644',
            owner='ec2-user:ec2-user',
        ) as original:
            restored = Schema__Exec__File__Transfer.from_json(original.json())
            assert restored.json() == original.json()
            assert type(restored.local_path) is Safe_Str__File__Path
            assert type(restored.owner) is Safe_Str__Process__Text
