from osbot_utils.type_safe.Type_Safe import Type_Safe
from osbot_utils.type_safe.type_safe_core.decorators.type_safe import type_safe

from sg_image_builder.schemas.exec.Schema__Exec__File__Transfer import (
    Schema__Exec__File__Transfer,
)
from sg_image_builder.schemas.exec.Schema__Exec__Request import Schema__Exec__Request
from sg_image_builder.schemas.exec.Schema__Exec__Result import Schema__Exec__Result


# Abstract base for any "run a command somewhere" provider. Per pack §04
# the synchronous `exec_command` is the headline feature: it returns a
# fully-populated Schema__Exec__Result with stdout / stderr / exit_code /
# elapsed_ms. No polling, no async machinery.
#
# Subclasses MUST override every method below. The base raises
# NotImplementedError following the pack's stated pattern (we keep using
# Type_Safe inheritance rather than `abc.ABC` because mixing metaclasses
# with Type_Safe is brittle and the pack's pattern is the proven path).
class Exec_Provider(Type_Safe):
    @type_safe
    def setup(self) -> 'Exec_Provider':
        raise NotImplementedError

    @type_safe
    def wait_ready(self, timeout_seconds: int = 60) -> bool:
        raise NotImplementedError

    @type_safe
    def exec_command(self, req: Schema__Exec__Request) -> Schema__Exec__Result:
        raise NotImplementedError

    @type_safe
    def copy_to(self, transfer: Schema__Exec__File__Transfer) -> Schema__Exec__Result:
        raise NotImplementedError

    @type_safe
    def copy_from(self, transfer: Schema__Exec__File__Transfer) -> Schema__Exec__Result:
        raise NotImplementedError

    @type_safe
    def teardown(self) -> None:
        raise NotImplementedError
