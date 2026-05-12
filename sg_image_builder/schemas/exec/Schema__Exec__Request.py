from osbot_utils.type_safe.primitives.core.Safe_UInt import Safe_UInt
from osbot_utils.type_safe.primitives.domains.files.safe_str.Safe_Str__File__Path import (
    Safe_Str__File__Path,
)
from osbot_utils.type_safe.Type_Safe import Type_Safe

from sg_image_builder.types.safe_str.Safe_Str__Process__Text import Safe_Str__Process__Text


# Input to Exec_Provider.exec_command(). Per pack §04 the canonical fields
# are command / cwd / env / timeout_seconds / user.
#
# Type calibration (v0.0.1__type-safe-usage-calibration.md):
#   command          -> Safe_Str__Process__Text     (L3; preserves shell chars)
#   cwd              -> Safe_Str__File__Path = None (L1; optional)
#   env              -> Dict[Process_Text, Process_Text] (L3; env keys and
#                                                          values can carry
#                                                          shell metacharacters)
#   timeout_seconds  -> Safe_UInt = 300             (L2; pack default)
#   user             -> Safe_Str__Process__Text = None (L3 sentinel; sudo target)
class Schema__Exec__Request(Type_Safe):
    command: Safe_Str__Process__Text
    cwd: Safe_Str__File__Path = None
    env: dict[Safe_Str__Process__Text, Safe_Str__Process__Text]
    timeout_seconds: Safe_UInt = 300
    user: Safe_Str__Process__Text = None  # type: ignore[assignment]
