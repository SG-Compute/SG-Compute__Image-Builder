import json
import subprocess
import time

from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id import (
    Safe_Str__Id,
)
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Slug import (
    Safe_Str__Slug,
)
from osbot_utils.type_safe.type_safe_core.decorators.type_safe import type_safe

from sg_image_builder.providers.exec.Exec_Provider import Exec_Provider
from sg_image_builder.schemas.exec.Schema__Exec__File__Transfer import (
    Schema__Exec__File__Transfer,
)
from sg_image_builder.schemas.exec.Schema__Exec__Request import Schema__Exec__Request
from sg_image_builder.schemas.exec.Schema__Exec__Result import Schema__Exec__Result


# Executes commands on an sg-compute-managed instance by shelling out to
# `sg lc exec <name> --region <r> -- <cmd>`. Per pack §04 we try, in order:
#
#   1. `sg lc exec ... --json` if the flag is supported
#   2. Best-effort text parsing of the legacy human-formatted output
#   3. Fail with a clear error if the output is unparseable
#
# Every fallback to (2) is a candidate item for the sg-compute team's
# `--json` backlog. The running list lives in
# humans/dinis_cruz/feedback-to-sg-compute.md (pack §11).
# Type calibration:
#   instance_name -> Safe_Str__Id    (L1; alphanumerics + - + _, e.g. 'my-vllm-1')
#                                     - raw Safe_Str strips `-` which mangles
#                                       real-world sg-compute names
#   region        -> Safe_Str__Slug  (L1; lowercase + - + digits, e.g. 'eu-west-2')
class Exec_Provider__Sg_Compute(Exec_Provider):
    instance_name: Safe_Str__Id
    region: Safe_Str__Slug
    use_json_flag: bool = True  # Set False to skip the --json attempt

    @type_safe
    def setup(self) -> 'Exec_Provider__Sg_Compute':
        return self  # No local-side setup; sg-compute owns the instance lifecycle

    @type_safe
    def wait_ready(self, timeout_seconds: int = 60) -> bool:
        # `sg lc list` would be the natural readiness check but we don't
        # want to silently swallow auth failures. For now, just attempt
        # a no-op `uname` and treat exit_code==0 as ready.
        probe = self.exec_command(Schema__Exec__Request(command='uname', timeout_seconds=timeout_seconds))
        return int(probe.exit_code) == 0

    @type_safe
    def exec_command(self, req: Schema__Exec__Request) -> Schema__Exec__Result:
        argv = ['sg', 'lc', 'exec', str(self.instance_name), '--region', str(self.region)]
        if self.use_json_flag:
            argv.append('--json')
        argv.extend(['--', str(req.command)])

        t0 = time.perf_counter()
        completed = subprocess.run(  # noqa: S603 (deliberate subprocess use)
            argv,
            capture_output=True,
            text=True,
            timeout=int(req.timeout_seconds),
            check=False,
        )
        elapsed_ms = int((time.perf_counter() - t0) * 1000)

        return self._build_result(req=req, completed=completed, elapsed_ms=elapsed_ms)

    def _build_result(
        self,
        req: Schema__Exec__Request,
        completed: subprocess.CompletedProcess,
        elapsed_ms: int,
    ) -> Schema__Exec__Result:
        # Path 1: --json output. If `sg lc exec --json` succeeded and the
        # body parses as JSON with the expected keys, use those values.
        if self.use_json_flag and completed.returncode == 0 and completed.stdout:
            try:
                payload = json.loads(completed.stdout)
                if isinstance(payload, dict) and 'exit_code' in payload:
                    return Schema__Exec__Result(
                        command=str(req.command),
                        stdout=payload.get('stdout', '') or '',
                        stderr=payload.get('stderr', '') or '',
                        exit_code=int(payload.get('exit_code', 0)),
                        elapsed_ms=int(payload.get('elapsed_ms', elapsed_ms)),
                    )
            except (json.JSONDecodeError, ValueError, TypeError):
                pass  # Fall through to text path

        # Path 2: legacy text output. We pass it through untouched - the
        # wrapper's exit_code IS the wrapped command's exit_code today, and
        # stdout / stderr already contain what the user would see at a
        # terminal. Refinements live behind a sg-compute --json flag.
        return Schema__Exec__Result(
            command=str(req.command),
            stdout=completed.stdout or '',
            stderr=completed.stderr or '',
            exit_code=int(completed.returncode),
            elapsed_ms=elapsed_ms,
        )

    @type_safe
    def copy_to(self, transfer: Schema__Exec__File__Transfer) -> Schema__Exec__Result:
        # `sg lc` doesn't expose a file-copy primitive yet (cf. feedback file).
        # When it does, this becomes a shell-out. For now: not implemented.
        raise NotImplementedError(
            'sg lc has no file-copy primitive yet - track in humans/dinis_cruz/feedback-to-sg-compute.md'
        )

    @type_safe
    def copy_from(self, transfer: Schema__Exec__File__Transfer) -> Schema__Exec__Result:
        raise NotImplementedError(
            'sg lc has no file-copy primitive yet - track in humans/dinis_cruz/feedback-to-sg-compute.md'
        )

    @type_safe
    def teardown(self) -> None:
        return None  # No teardown - sg-compute owns the lifecycle
