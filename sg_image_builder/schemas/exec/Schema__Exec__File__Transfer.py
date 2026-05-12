from osbot_utils.type_safe.primitives.domains.files.safe_str.Safe_Str__File__Path import (
    Safe_Str__File__Path,
)
from osbot_utils.type_safe.Type_Safe import Type_Safe

from sg_image_builder.types.safe_str.Safe_Str__Process__Text import Safe_Str__Process__Text


# Input to Exec_Provider.copy_to() / copy_from(). Per pack §04.
#
# Type calibration:
#   local_path  -> Safe_Str__File__Path                  (L1; required for both ops)
#   remote_path -> Safe_Str__File__Path                  (L1)
#   mode        -> Safe_Str__Process__Text = None        (L3; chmod mode 'a+x' etc.)
#   owner       -> Safe_Str__Process__Text = None        (L3; chown spec 'user:group' contains `:`)
class Schema__Exec__File__Transfer(Type_Safe):
    local_path: Safe_Str__File__Path
    remote_path: Safe_Str__File__Path
    mode: Safe_Str__Process__Text = None  # type: ignore[assignment]
    owner: Safe_Str__Process__Text = None  # type: ignore[assignment]
