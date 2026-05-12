import json
import subprocess
from unittest import TestCase
from unittest.mock import patch

from sg_image_builder.providers.exec.Exec_Provider__Sg_Compute import Exec_Provider__Sg_Compute
from sg_image_builder.schemas.exec.Schema__Exec__File__Transfer import (
    Schema__Exec__File__Transfer,
)
from sg_image_builder.schemas.exec.Schema__Exec__Request import Schema__Exec__Request


def _completed(stdout: str = '', stderr: str = '', returncode: int = 0) -> subprocess.CompletedProcess:
    return subprocess.CompletedProcess(args=['sg', 'lc'], returncode=returncode, stdout=stdout, stderr=stderr)


class test_Exec_Provider__Sg_Compute(TestCase):
    def setUp(self):
        self.provider = Exec_Provider__Sg_Compute(
            instance_name='my-vllm-1',
            region='eu-west-2',
        ).setup()

    def test__init__preserves_hyphens(self):  # Regression: raw Safe_Str strips `-`
        assert str(self.provider.instance_name) == 'my-vllm-1'
        assert str(self.provider.region) == 'eu-west-2'

    def test__init__defaults_use_json_flag_true(self):  # Try --json first per pack §04
        assert self.provider.use_json_flag is True

    @patch('subprocess.run')
    def test__exec_command__appends_json_flag_when_enabled(self, mock_run):  # The CLI arglist contains --json
        mock_run.return_value = _completed(stdout='', returncode=0)
        self.provider.exec_command(Schema__Exec__Request(command='uname'))
        argv = mock_run.call_args[0][0]
        assert '--json' in argv

    @patch('subprocess.run')
    def test__exec_command__omits_json_flag_when_disabled(self, mock_run):
        mock_run.return_value = _completed(stdout='', returncode=0)
        Exec_Provider__Sg_Compute(
            instance_name='x',
            region='r',
            use_json_flag=False,
        ).exec_command(Schema__Exec__Request(command='uname'))
        argv = mock_run.call_args[0][0]
        assert '--json' not in argv

    @patch('subprocess.run')
    def test__exec_command__path1_json_payload(self, mock_run):  # Structured JSON path returns nested fields
        payload = {
            'stdout': 'Linux\n',
            'stderr': '',
            'exit_code': 0,
            'elapsed_ms': 87,
        }
        mock_run.return_value = _completed(stdout=json.dumps(payload), returncode=0)
        r = self.provider.exec_command(Schema__Exec__Request(command='uname'))
        assert str(r.stdout) == 'Linux\n'
        assert r.exit_code == 0
        assert r.elapsed_ms == 87

    @patch('subprocess.run')
    def test__exec_command__path2_text_fallback(self, mock_run):  # Non-JSON output flows through verbatim
        mock_run.return_value = _completed(stdout='Linux 6.1\n', stderr='', returncode=0)
        r = self.provider.exec_command(Schema__Exec__Request(command='uname'))
        assert 'Linux 6.1' in str(r.stdout)
        assert r.exit_code == 0

    @patch('subprocess.run')
    def test__exec_command__nonzero_returncode_flows_through(self, mock_run):
        mock_run.return_value = _completed(stdout='', stderr='auth failed\n', returncode=2)
        r = self.provider.exec_command(Schema__Exec__Request(command='whoami'))
        assert r.exit_code == 2
        assert 'auth failed' in str(r.stderr)

    @patch('subprocess.run')
    def test__exec_command__invalid_json_falls_to_text_path(self, mock_run):  # Malformed JSON shouldn't crash
        mock_run.return_value = _completed(stdout='not valid json{', returncode=0)
        r = self.provider.exec_command(Schema__Exec__Request(command='whoami'))
        assert 'not valid json' in str(r.stdout)

    @patch('subprocess.run')
    def test__exec_command__cmd_passed_after_double_dash(
        self, mock_run
    ):  # The command goes after `--` so sg lc doesn't eat its flags
        mock_run.return_value = _completed()
        self.provider.exec_command(Schema__Exec__Request(command='uname -a'))
        argv = mock_run.call_args[0][0]
        dash_idx = argv.index('--')
        assert argv[dash_idx + 1] == 'uname -a'

    def test__copy_to__not_implemented(self):  # No primitive in `sg lc` yet
        with self.assertRaises(NotImplementedError):
            self.provider.copy_to(Schema__Exec__File__Transfer())

    def test__copy_from__not_implemented(self):
        with self.assertRaises(NotImplementedError):
            self.provider.copy_from(Schema__Exec__File__Transfer())

    def test__teardown__noop(self):
        assert self.provider.teardown() is None
