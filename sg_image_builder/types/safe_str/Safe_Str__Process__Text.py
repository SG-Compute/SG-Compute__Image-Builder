from osbot_utils.type_safe.primitives.domains.http.safe_str.Safe_Str__Http__Text import (
    Safe_Str__Http__Text,
)


# Text captured from / about a subprocess (the command we ran, its stdout,
# its stderr). The closest existing OSBot primitive is Safe_Str__Http__Text:
# 1 MB max, replaces control chars but keeps tab/newline/CR.
#
# Two changes for the subprocess use case:
#   - max_length raised to 10 MB - real build output is bigger than HTTP
#     bodies. The 1 MB limit silently truncates `pip install`-scale logs.
#   - trim_whitespace=False - trailing newlines on stdout carry meaning
#     (POSIX text-file convention; absence of trailing newline is often
#     significant). The default True would silently drop them.
#
# Both deltas are real findings from the M1 PR1 smoke test; see the
# v0.0.1 type_safe calibration review for the methodology rationale.
class Safe_Str__Process__Text(Safe_Str__Http__Text):
    max_length = 10 * 1024 * 1024
    trim_whitespace = False
