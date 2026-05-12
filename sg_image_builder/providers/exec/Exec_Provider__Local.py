import shlex
import shutil
import subprocess
import time

from osbot_utils.type_safe.type_safe_core.decorators.type_safe import type_safe

from sg_image_builder.providers.exec.Exec_Provider import Exec_Provider
from sg_image_builder.schemas.exec.Schema__Exec__File__Transfer import (
    Schema__Exec__File__Transfer,
)
from sg_image_builder.schemas.exec.Schema__Exec__Request import Schema__Exec__Request
from sg_image_builder.schemas.exec.Schema__Exec__Result import Schema__Exec__Result


# Runs commands on the local machine via subprocess.run. Useful for:
#   - dev / iteration without needing SSH or sg-compute set up
#   - integration tests that need a real exec backend but no remote
#
# Not in the pack §04 catalogue but we already accepted it in PR1's
# Enum__Exec_Provider_Kind.LOCAL - this is the implementation.
#
# Security note: command is shlex.split'd, NOT passed through a shell.
# Callers wanting shell features (pipes, globbing) must run via
# `sh -c '<expr>'` explicitly.
class Exec_Provider__Local(Exec_Provider):
    @type_safe
    def setup(self) -> 'Exec_Provider__Local':
        return self  # No setup needed for local exec

    @type_safe
    def wait_ready(self, timeout_seconds: int = 60) -> bool:
        return True  # The local machine is always ready

    @type_safe
    def exec_command(self, req: Schema__Exec__Request) -> Schema__Exec__Result:
        argv = shlex.split(str(req.command))

        merged_env = None
        if req.env:
            merged_env = {str(k): str(v) for k, v in req.env.items()}

        t0 = time.perf_counter()
        completed = subprocess.run(  # noqa: S603 (deliberate subprocess use)
            argv,
            capture_output=True,
            text=True,
            cwd=str(req.cwd) if req.cwd else None,
            env=merged_env,
            timeout=int(req.timeout_seconds),
            check=False,  # never raise; we return the result
        )
        elapsed_ms = int((time.perf_counter() - t0) * 1000)

        return Schema__Exec__Result(
            command=str(req.command),
            stdout=completed.stdout or '',
            stderr=completed.stderr or '',
            exit_code=int(completed.returncode),
            elapsed_ms=elapsed_ms,
        )

    @type_safe
    def copy_to(self, transfer: Schema__Exec__File__Transfer) -> Schema__Exec__Result:
        # "Local" copy_to is a same-machine file copy.
        t0 = time.perf_counter()
        shutil.copy2(str(transfer.local_path), str(transfer.remote_path))
        elapsed_ms = int((time.perf_counter() - t0) * 1000)
        return Schema__Exec__Result(
            command=f'cp {transfer.local_path} {transfer.remote_path}',
            stdout='',
            stderr='',
            exit_code=0,
            elapsed_ms=elapsed_ms,
        )

    @type_safe
    def copy_from(self, transfer: Schema__Exec__File__Transfer) -> Schema__Exec__Result:
        # For Local, copy_from is symmetric with copy_to.
        t0 = time.perf_counter()
        shutil.copy2(str(transfer.remote_path), str(transfer.local_path))
        elapsed_ms = int((time.perf_counter() - t0) * 1000)
        return Schema__Exec__Result(
            command=f'cp {transfer.remote_path} {transfer.local_path}',
            stdout='',
            stderr='',
            exit_code=0,
            elapsed_ms=elapsed_ms,
        )

    @type_safe
    def teardown(self) -> None:
        return None  # No teardown needed
