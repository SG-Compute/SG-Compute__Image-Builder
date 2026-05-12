from osbot_utils.type_safe.type_safe_core.decorators.type_safe import type_safe

from sg_image_builder.providers.exec.Exec_Provider import Exec_Provider
from sg_image_builder.schemas.exec.Schema__Exec__File__Transfer import (
    Schema__Exec__File__Transfer,
)
from sg_image_builder.schemas.exec.Schema__Exec__Request import Schema__Exec__Request
from sg_image_builder.schemas.exec.Schema__Exec__Result import Schema__Exec__Result


# In-memory test double. Records every call into `command_log` / `transfer_log`
# and returns canned responses keyed by the command string.
#
# Pattern lifted from the dev pack §04 (which itself lifts from
# SG_Send__Deploy's SSH__Execute__Twin). Used in tests that exercise
# higher-level code without spinning up subprocess or sg-compute.
class Exec_Provider__Twin(Exec_Provider):
    command_log: list[Schema__Exec__Request]
    transfer_log: list[Schema__Exec__File__Transfer]
    canned_responses: dict[str, Schema__Exec__Result]
    default_exit_code: int = 0  # Used when no canned response matches

    @type_safe
    def setup(self) -> 'Exec_Provider__Twin':
        return self

    @type_safe
    def wait_ready(self, timeout_seconds: int = 60) -> bool:
        return True  # Twins are always ready

    @type_safe
    def set_response(self, command: str, result: Schema__Exec__Result) -> 'Exec_Provider__Twin':
        self.canned_responses[command] = result
        return self  # Chainable for fixture setup

    @type_safe
    def exec_command(self, req: Schema__Exec__Request) -> Schema__Exec__Result:
        self.command_log.append(req)
        cmd_str = str(req.command)
        if cmd_str in self.canned_responses:
            return self.canned_responses[cmd_str]
        return Schema__Exec__Result(
            command=cmd_str,
            stdout='',
            stderr='',
            exit_code=int(self.default_exit_code),
            elapsed_ms=0,
        )

    @type_safe
    def copy_to(self, transfer: Schema__Exec__File__Transfer) -> Schema__Exec__Result:
        self.transfer_log.append(transfer)
        return Schema__Exec__Result(
            command=f'copy_to {transfer.local_path} -> {transfer.remote_path}',
            stdout='',
            stderr='',
            exit_code=0,
            elapsed_ms=0,
        )

    @type_safe
    def copy_from(self, transfer: Schema__Exec__File__Transfer) -> Schema__Exec__Result:
        self.transfer_log.append(transfer)
        return Schema__Exec__Result(
            command=f'copy_from {transfer.remote_path} -> {transfer.local_path}',
            stdout='',
            stderr='',
            exit_code=0,
            elapsed_ms=0,
        )

    @type_safe
    def teardown(self) -> None:
        return None
