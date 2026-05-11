import re
import subprocess
import sys
from pathlib import Path

from typer.testing import CliRunner

import sg_image_builder
from sg_image_builder.cli.app import app

# PEP 440 release segment (https://peps.python.org/pep-0440/) - minimal regex
# for the shape sgi uses: N(.N)*[.devN | aN | bN | rcN | .postN].
PEP440_RE = re.compile(r'^\d+(\.\d+)*([.\-]?(a|b|rc|dev|post)\d+)?$')


def test_version_file_exists_and_matches_v_prefix() -> None:
    version_path = Path(sg_image_builder.__file__).parent / 'version'
    assert version_path.is_file()
    assert version_path.read_text().strip().startswith('v')


def test_module_version_attribute_is_pep440() -> None:
    assert PEP440_RE.match(sg_image_builder.__version__), (
        f'__version__ {sg_image_builder.__version__!r} is not PEP 440 compliant'
    )


def test_module_version_strips_leading_v() -> None:
    assert not sg_image_builder.__version__.startswith('v')
    assert sg_image_builder.version.startswith('v')
    assert sg_image_builder.version.lstrip('v') == sg_image_builder.__version__


def test_cli_version_flag_via_typer_runner() -> None:
    runner = CliRunner()
    result = runner.invoke(app, ['--version'])
    assert result.exit_code == 0
    assert sg_image_builder.version in result.stdout


def test_cli_version_subcommand_via_typer_runner() -> None:
    runner = CliRunner()
    result = runner.invoke(app, ['version'])
    assert result.exit_code == 0
    assert sg_image_builder.version in result.stdout


def test_cli_doctor_subcommand_runs_in_m0() -> None:
    runner = CliRunner()
    result = runner.invoke(app, ['doctor'])
    assert result.exit_code == 0
    assert sg_image_builder.version in result.stdout
    assert 'M0 bootstrap' in result.stdout


def test_cli_version_via_python_m() -> None:
    # End-to-end smoke: invoke as a subprocess so we exercise the entry point.
    result = subprocess.run(
        [sys.executable, '-m', 'sg_image_builder.cli.app', '--version'],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, (result.stdout, result.stderr)
    assert sg_image_builder.version in result.stdout
