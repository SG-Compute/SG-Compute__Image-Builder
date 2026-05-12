import re

from osbot_utils.type_safe.primitives.core.enums.Enum__Safe_Str__Regex_Mode import (
    Enum__Safe_Str__Regex_Mode,
)
from osbot_utils.type_safe.primitives.core.Safe_Str import Safe_Str


# OCI image-repository name grammar (distribution spec):
#   - lowercase letters, digits, separators `.` `_` `__` `-`
#   - components joined with `/`
#   - each component matches: [a-z0-9]+(?:(?:[._]|__|[-]+)[a-z0-9]+)*
# https://github.com/opencontainers/distribution-spec/blob/main/spec.md#pulling-manifests
#
# We pick 255 as the max because that's the maximum total length the
# Docker / OCI ecosystem accepts in practice.
class Safe_Str__Image_Repository(Safe_Str):
    max_length = 255
    regex = re.compile(
        r'^[a-z0-9]+(?:(?:[._]|__|-+)[a-z0-9]+)*'
        r'(?:/[a-z0-9]+(?:(?:[._]|__|-+)[a-z0-9]+)*)*$'
    )
    regex_mode = Enum__Safe_Str__Regex_Mode.MATCH
    strict_validation = True
    # allow_empty=True: '' is the "not yet set" sentinel for Type_Safe auto-init;
    # non-empty values still validated against the OCI grammar above.
    allow_empty = True
