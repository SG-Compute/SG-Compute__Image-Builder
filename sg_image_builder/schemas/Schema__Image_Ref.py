from osbot_utils.type_safe.primitives.domains.web.safe_str.Safe_Str__Url import Safe_Str__Url
from osbot_utils.type_safe.Type_Safe import Type_Safe

from sg_image_builder.types.safe_str.Safe_Str__Image_Digest import Safe_Str__Image_Digest
from sg_image_builder.types.safe_str.Safe_Str__Image_Repository import Safe_Str__Image_Repository
from sg_image_builder.types.safe_str.Safe_Str__Image_Tag import Safe_Str__Image_Tag


# An OCI image reference: [<registry>/]<repository>[:<tag>][@<digest>]
#
# Type calibration (per dev review v0.0.1__type-safe-usage-calibration.md;
# delta from PR1 smoke test - 4 L3 primitives now, not 2):
#   registry   -> Safe_Str__Url               (L1; optional)
#   repository -> Safe_Str__Image_Repository  (L3; Safe_Str__Text mangled `/`)
#   tag        -> Safe_Str__Image_Tag         (L3; OCI tag grammar; defaults to 'latest')
#   digest     -> Safe_Str__Image_Digest      (L3; sha256/sha512 + hex)
# mypy notes: the `'latest'` and `None` defaults are Type_Safe-idiomatic
# (auto-converted at runtime; see Type_Safe canon §5). mypy can't see the
# runtime conversion so we narrow-suppress the [assignment] error here.
class Schema__Image_Ref(Type_Safe):
    registry: Safe_Str__Url = None
    repository: Safe_Str__Image_Repository
    tag: Safe_Str__Image_Tag = 'latest'  # type: ignore[assignment]
    digest: Safe_Str__Image_Digest = None  # type: ignore[assignment]
