import re

from osbot_utils.type_safe.primitives.core.enums.Enum__Safe_Str__Regex_Mode import (
    Enum__Safe_Str__Regex_Mode,
)
from osbot_utils.type_safe.primitives.core.Safe_Str import Safe_Str


# OCI image-digest grammar (image-spec):
#   <algorithm>:<encoded>
#   - sha256: 64 lowercase hex chars
#   - sha512: 128 lowercase hex chars
# https://github.com/opencontainers/image-spec/blob/main/descriptor.md#digests
#
# Only sha256 and sha512 are accepted (the two algorithms in the OCI spec).
class Safe_Str__Image_Digest(Safe_Str):
    max_length = len('sha512:') + 128
    regex = re.compile(r'^(?:sha256:[a-f0-9]{64}|sha512:[a-f0-9]{128})$')
    regex_mode = Enum__Safe_Str__Regex_Mode.MATCH
    strict_validation = True
    allow_empty = False
