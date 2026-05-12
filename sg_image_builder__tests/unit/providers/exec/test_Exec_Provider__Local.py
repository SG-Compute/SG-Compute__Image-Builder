import subprocess
import tempfile
from pathlib import Path
from unittest import TestCase

from sg_image_builder.providers.exec.Exec_Provider__Local import Exec_Provider__Local
from sg_image_builder.schemas.exec.Schema__Exec__File__Transfer import (
    Schema__Exec__File__Transfer,
)
from sg_image_builder.schemas.exec.Schema__Exec__Request import Schema__Exec__Request


class test_Exec_Provider__Local(TestCase):
    def setUp(self):
        self.provider = Exec_Provider__Local().setup()

    def tearDown(self):
        self.provider.teardown()

    def test__init__(self):  # Base + subclass identity
        assert type(self.provider) is Exec_Provider__Local

    def test__wait_ready__always_true(self):  # Local machine is always reachable
        assert self.provider.wait_ready() is True

    def test__exec_command__success(self):  # Round-trips through the real local shell
        r = self.provider.exec_command(Schema__Exec__Request(command='echo hello'))
        assert r.exit_code == 0
        assert 'hello' in str(r.stdout)
        assert r.elapsed_ms >= 0

    def test__exec_command__nonzero_exit(self):  # `false` exits with code 1
        r = self.provider.exec_command(Schema__Exec__Request(command='false'))
        assert r.exit_code == 1

    def test__exec_command__captures_stderr(self):  # `ls` of a missing path writes to stderr
        r = self.provider.exec_command(Schema__Exec__Request(command='ls /nonexistent_sgi_test_path_xyz'))
        assert r.exit_code != 0
        assert str(r.stderr) != ''

    def test__exec_command__env_passthrough(self):  # Env dict reaches the spawned process
        r = self.provider.exec_command(
            Schema__Exec__Request(
                command='/bin/sh -c "echo SGI_TEST=$SGI_TEST"',
                env={'SGI_TEST': 'value_from_test'},
            )
        )
        assert 'SGI_TEST=value_from_test' in str(r.stdout)

    def test__exec_command__cwd(self):  # cwd is honoured
        with tempfile.TemporaryDirectory() as tmp:
            r = self.provider.exec_command(Schema__Exec__Request(command='pwd', cwd=tmp))
            assert tmp in str(r.stdout)

    def test__exec_command__timeout(self):  # Long command times out
        with self.assertRaises(subprocess.TimeoutExpired):
            self.provider.exec_command(Schema__Exec__Request(command='sleep 5', timeout_seconds=1))

    def test__copy_to__round_trip(self):  # copy_to is a same-machine file copy
        with tempfile.TemporaryDirectory() as tmp:
            src = Path(tmp) / 'src.txt'
            dst = Path(tmp) / 'dst.txt'
            src.write_text('hello world')
            r = self.provider.copy_to(Schema__Exec__File__Transfer(local_path=str(src), remote_path=str(dst)))
            assert r.exit_code == 0
            assert dst.read_text() == 'hello world'

    def test__copy_from__round_trip(self):  # copy_from is the inverse
        with tempfile.TemporaryDirectory() as tmp:
            remote = Path(tmp) / 'remote.txt'
            local = Path(tmp) / 'local.txt'
            remote.write_text('payload')
            r = self.provider.copy_from(Schema__Exec__File__Transfer(local_path=str(local), remote_path=str(remote)))
            assert r.exit_code == 0
            assert local.read_text() == 'payload'

    def test__teardown__noop(self):  # No exception, returns None
        assert self.provider.teardown() is None
