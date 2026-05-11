"""Build dist/sgi.zipapp from the sg_image_builder package.

M0 scaffolding: produces a runnable but un-vendored zipapp. Dependency
vendoring lands in M12 when the release artefact is hardened.

Usage:
    python scripts/build_zipapp.py
"""
from __future__ import annotations

import shutil
import zipapp
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
SRC       = REPO_ROOT / 'sg_image_builder'
STAGING   = REPO_ROOT / 'dist' / 'staging'
TARGET    = REPO_ROOT / 'dist' / 'sgi.zipapp'


def build() -> Path:
    STAGING.parent.mkdir(parents=True, exist_ok=True)
    if STAGING.exists():
        shutil.rmtree(STAGING)
    STAGING.mkdir(parents=True)

    # Copy package source verbatim
    shutil.copytree(SRC, STAGING / 'sg_image_builder')

    # TODO (M12): vendor non-stdlib dependencies (osbot-utils, osbot-aws,
    # typer, rich, zstandard) into STAGING/ so the zipapp is self-contained
    # offline (principle P19, P20).

    zipapp.create_archive(
        source     = STAGING,
        target     = TARGET,
        interpreter= '/usr/bin/env python3',
        main       = 'sg_image_builder.cli.app:app',
    )
    TARGET.chmod(0o755)
    return TARGET


if __name__ == '__main__':
    out = build()
    print(f'built: {out}')
