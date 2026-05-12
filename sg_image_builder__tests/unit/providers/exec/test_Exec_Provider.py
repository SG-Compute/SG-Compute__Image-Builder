from unittest import TestCase

from osbot_utils.type_safe.Type_Safe import Type_Safe

from sg_image_builder.providers.exec.Exec_Provider import Exec_Provider
from sg_image_builder.schemas.exec.Schema__Exec__File__Transfer import (
    Schema__Exec__File__Transfer,
)
from sg_image_builder.schemas.exec.Schema__Exec__Request import Schema__Exec__Request


class test_Exec_Provider(TestCase):
    def test__init__(self):  # Base is a plain Type_Safe; constructible
        with Exec_Provider() as _:
            assert type(_) is Exec_Provider
            assert isinstance(_, Type_Safe)

    def test__setup__raises_NotImplementedError(self):
        with self.assertRaises(NotImplementedError):
            Exec_Provider().setup()

    def test__wait_ready__raises_NotImplementedError(self):
        with self.assertRaises(NotImplementedError):
            Exec_Provider().wait_ready()

    def test__exec_command__raises_NotImplementedError(self):
        with self.assertRaises(NotImplementedError):
            Exec_Provider().exec_command(Schema__Exec__Request())

    def test__copy_to__raises_NotImplementedError(self):
        with self.assertRaises(NotImplementedError):
            Exec_Provider().copy_to(Schema__Exec__File__Transfer())

    def test__copy_from__raises_NotImplementedError(self):
        with self.assertRaises(NotImplementedError):
            Exec_Provider().copy_from(Schema__Exec__File__Transfer())

    def test__teardown__raises_NotImplementedError(self):
        with self.assertRaises(NotImplementedError):
            Exec_Provider().teardown()
