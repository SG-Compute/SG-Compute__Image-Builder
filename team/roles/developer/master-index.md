# Developer — Master Index

_Maintained by the Developer role with help from the Librarian._

## Latest reviews

- [v0.0.1 - M1 PR1: types + first schemas](reviews/05/12/v0.0.1__m1-pr1__types-and-schemas.md) - 12 May 2026 (latest)
- [v0.0.1 - Type_Safe usage calibration](reviews/05/11/v0.0.1__type-safe-usage-calibration.md) - 11 May 2026 (+ 12 May addendum)
- [v0.0.1 - M0 bootstrap implementation plan](reviews/05/11/v0.0.1__implementation-plan__m0-bootstrap.md) - 11 May 2026

## Decisions

- **Type_Safe ladder (v1, 11 May):** climb from existing OSBot domain primitives -> generic Safe_* -> custom Safe_*__X only when a non-trivial regex/range needs enforcing. Closed sets become `Enum` / `Literal`, never `Safe_Str__X` with an enumerating regex.
- **L3 trigger refined (v1.1, 12 May addendum):** ALSO climb to L3 when an L1 primitive *silently transforms* input (REPLACE-mode regex, `trim_whitespace=True`). Inspect `regex` / `regex_mode` / `trim_whitespace` before trusting a primitive. PR1 discovered `Safe_Str__Text` strips `/` and `Safe_Str__Http__Text` drops trailing newlines.

## Active items

- M1 PR1 has landed on the working branch: 4 L3 primitives, 2 enums, 2 schemas, 68 unit tests. ruff/mypy/pytest all clean.
- M1 PR2: lift `Exec_Provider` base + `Exec_Provider__Local` + `Exec_Provider__Sg_Compute` from sister repo. Blocked on spike-status confirmation per HANDOVER.
