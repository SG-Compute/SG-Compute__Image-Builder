import re

from osbot_utils.type_safe.primitives.core.enums.Enum__Safe_Str__Regex_Mode import (
    Enum__Safe_Str__Regex_Mode,
)
from osbot_utils.type_safe.primitives.core.Safe_Str import Safe_Str


# OCI image-tag grammar (distribution spec):
#   "A tag name must be valid ASCII and may contain lowercase and uppercase
#    letters, digits, underscores, periods and dashes. A tag name may not
#    start with a period or a dash and may contain a maximum of 128 characters."
# https://github.com/opencontainers/distribution-spec/blob/main/spec.md#pulling-manifests
class Safe_Str__Image_Tag(Safe_Str):
    max_length = 128
    regex = re.compile(r'^[a-zA-Z0-9_][a-zA-Z0-9._-]{0,127}$')
    regex_mode = Enum__Safe_Str__Regex_Mode.MATCH
    strict_validation = True
    allow_empty = False
