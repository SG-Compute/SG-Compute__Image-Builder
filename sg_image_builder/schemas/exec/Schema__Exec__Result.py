from osbot_utils.type_safe.primitives.core.Safe_Int import Safe_Int
from osbot_utils.type_safe.primitives.core.Safe_UInt import Safe_UInt
from osbot_utils.type_safe.Type_Safe import Type_Safe

from sg_image_builder.types.safe_str.Safe_Str__Process__Text import Safe_Str__Process__Text


# The result of executing an external command (subprocess.run, `sg lc exec`,
# etc.). Field shape mirrors the JSON we'd ideally get back from
# `sg lc exec --json` (see humans/dinis_cruz/feedback-to-sg-compute.md).
#
# Type calibration (per dev review v0.0.1__type-safe-usage-calibration.md;
# delta from PR1 smoke test):
#   command/stdout/stderr -> Safe_Str__Process__Text (L3)
#       Safe_Str__Text mangles `/`, Safe_Str__Http__Text trims trailing
#       whitespace - both lose data for exec capture. The L3 type
#       preserves them.
#   exit_code  -> Safe_Int    (L2; signed on Unix - signal kills give -N)
#   elapsed_ms -> Safe_UInt   (L2; duration is always >= 0)
class Schema__Exec__Result(Type_Safe):
    command: Safe_Str__Process__Text
    stdout: Safe_Str__Process__Text
    stderr: Safe_Str__Process__Text
    exit_code: Safe_Int
    elapsed_ms: Safe_UInt
