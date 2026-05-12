from unittest import TestCase

from sg_image_builder.providers.exec.Exec_Provider__Twin import Exec_Provider__Twin
from sg_image_builder.schemas.exec.Schema__Exec__File__Transfer import (
    Schema__Exec__File__Transfer,
)
from sg_image_builder.schemas.exec.Schema__Exec__Request import Schema__Exec__Request
from sg_image_builder.schemas.exec.Schema__Exec__Result import Schema__Exec__Result


class test_Exec_Provider__Twin(TestCase):
    def setUp(self):
        self.provider = Exec_Provider__Twin().setup()

    def test__init__(self):  # Empty logs and dict by default
        with Exec_Provider__Twin() as _:
            assert type(_) is Exec_Provider__Twin
            assert list(_.command_log) == []
            assert list(_.transfer_log) == []
            assert dict(_.canned_responses) == {}
            assert _.default_exit_code == 0

    def test__wait_ready__always_true(self):
        assert self.provider.wait_ready() is True

    def test__exec_command__default_response(self):  # No canned response -> default empty
        r = self.provider.exec_command(Schema__Exec__Request(command='echo hi'))
        assert r.exit_code == 0
        assert str(r.stdout) == ''
        assert str(r.stderr) == ''

    def test__exec_command__canned_response(self):  # Canned response returned verbatim
        canned = Schema__Exec__Result(command='whoami', stdout='ec2-user\n', exit_code=0, elapsed_ms=5)
        self.provider.set_response('whoami', canned)
        r = self.provider.exec_command(Schema__Exec__Request(command='whoami'))
        assert str(r.stdout) == 'ec2-user\n'
        assert r.elapsed_ms == 5

    def test__exec_command__records_in_log(self):  # Every call appended
        self.provider.exec_command(Schema__Exec__Request(command='a'))
        self.provider.exec_command(Schema__Exec__Request(command='b'))
        assert len(self.provider.command_log) == 2
        assert str(self.provider.command_log[0].command) == 'a'
        assert str(self.provider.command_log[1].command) == 'b'

    def test__copy_to__records_in_transfer_log(self):  # File-transfer calls also recorded
        t = Schema__Exec__File__Transfer(local_path='/tmp/a', remote_path='/opt/a')
        r = self.provider.copy_to(t)
        assert r.exit_code == 0
        assert len(self.provider.transfer_log) == 1
        assert str(self.provider.transfer_log[0].local_path) == '/tmp/a'
        assert str(self.provider.transfer_log[0].remote_path) == '/opt/a'

    def test__copy_from__records_in_transfer_log(self):  # Same for copy_from
        t = Schema__Exec__File__Transfer(local_path='/tmp/a', remote_path='/opt/a')
        r = self.provider.copy_from(t)
        assert r.exit_code == 0
        assert len(self.provider.transfer_log) == 1

    def test__custom_default_exit_code(self):  # Use to simulate a failing target
        twin = Exec_Provider__Twin(default_exit_code=42).setup()
        r = twin.exec_command(Schema__Exec__Request(command='x'))
        assert r.exit_code == 42

    def test__teardown__noop(self):
        assert self.provider.teardown() is None

    def test__set_response__is_chainable(self):  # Returns self for fixture setup ergonomics
        twin = Exec_Provider__Twin()
        chained = twin.set_response('a', Schema__Exec__Result(command='a', stdout='A')).set_response(
            'b', Schema__Exec__Result(command='b', stdout='B')
        )
        assert chained is twin
        assert 'a' in twin.canned_responses
        assert 'b' in twin.canned_responses
