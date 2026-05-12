from enum import Enum


# sgi's own CLI exit codes. Intentionally minimal at PR1 - extended as
# specific failure modes surface during M1+ (spec not found, provider
# unavailable, etc.).
#
# Note: the `exit_code` field on Schema__Exec__Result is a plain Safe_Int -
# it captures the return code of arbitrary external commands and is NOT
# constrained to this enum.
class Enum__Exit_Code(int, Enum):
    SUCCESS = 0  # Successful completion
    GENERIC_ERROR = 1  # Unspecified failure
    CLI_USAGE_ERROR = 2  # Invalid CLI invocation (Typer convention)
    INTERRUPTED = 130  # User cancelled (SIGINT / Ctrl-C)

    def __str__(self) -> str:
        return str(self.value)
