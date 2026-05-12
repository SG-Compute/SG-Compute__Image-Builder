from unittest import TestCase

from osbot_utils.testing.__ import __
from osbot_utils.type_safe.Type_Safe import Type_Safe

from sg_image_builder.schemas.Schema__Image_Ref import Schema__Image_Ref
from sg_image_builder.types.safe_str.Safe_Str__Image_Digest import Safe_Str__Image_Digest
from sg_image_builder.types.safe_str.Safe_Str__Image_Repository import Safe_Str__Image_Repository
from sg_image_builder.types.safe_str.Safe_Str__Image_Tag import Safe_Str__Image_Tag

SHA256 = 'sha256:' + 'a' * 64


class test_Schema__Image_Ref(TestCase):
    def test__init__(self):  # Auto-init: registry/digest=None, tag='latest', repo=''
        with Schema__Image_Ref() as _:
            assert type(_) is Schema__Image_Ref
            assert isinstance(_, Type_Safe)
            assert _.obj() == __(registry=None, repository='', tag='latest', digest=None)

    def test__init__minimal(self):  # Just the repository - tag defaults to OCI 'latest'
        with Schema__Image_Ref(repository='library/ubuntu') as _:
            assert _.obj() == __(registry=None, repository='library/ubuntu', tag='latest', digest=None)
            assert type(_.repository) is Safe_Str__Image_Repository
            assert type(_.tag) is Safe_Str__Image_Tag

    def test__init__full(self):  # All fields populated
        with Schema__Image_Ref(
            registry='https://registry.example.com', repository='org/sub/app', tag='v1.2.3', digest=SHA256
        ) as _:
            assert _.obj() == __(
                registry='https://registry.example.com', repository='org/sub/app', tag='v1.2.3', digest=SHA256
            )
            assert type(_.digest) is Safe_Str__Image_Digest

    def test__preserves_repository_slashes(self):  # Regression: Safe_Str__Text replaces `/` with `_`
        with Schema__Image_Ref(repository='library/ubuntu') as _:
            assert '/' in str(_.repository)

    def test__rejects_invalid_repository(self):  # Uppercase not allowed by OCI grammar
        with self.assertRaises(ValueError):
            Schema__Image_Ref(repository='Library/Ubuntu')

    def test__rejects_invalid_tag(self):  # Tag starting with `.` is invalid
        with self.assertRaises(ValueError):
            Schema__Image_Ref(repository='ubuntu', tag='.bad')

    def test__rejects_invalid_digest(self):  # md5 not in OCI distribution-spec
        with self.assertRaises(ValueError):
            Schema__Image_Ref(repository='ubuntu', digest='md5:' + 'a' * 32)

    def test__json_round_trip(self):  # Serialise + deserialise yields identical content + types
        with Schema__Image_Ref(repository='org/app', tag='v1.0', digest=SHA256) as original:
            restored = Schema__Image_Ref.from_json(original.json())
            assert restored.json() == original.json()
            assert type(restored.repository) is Safe_Str__Image_Repository
            assert type(restored.tag) is Safe_Str__Image_Tag
            assert type(restored.digest) is Safe_Str__Image_Digest
