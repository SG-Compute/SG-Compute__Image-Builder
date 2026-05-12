# Developer — Master Index

_Maintained by the Developer role with help from the Librarian._

## Latest reviews

- [v0.0.1 - M1 PR2: Exec_Provider family](reviews/05/12/v0.0.1__m1-pr2__exec-providers.md) - 12 May 2026 (latest)
- [v0.0.1 - M1 PR1: types + first schemas](reviews/05/12/v0.0.1__m1-pr1__types-and-schemas.md) - 12 May 2026
- [v0.0.1 - Type_Safe usage calibration](reviews/05/11/v0.0.1__type-safe-usage-calibration.md) - 11 May 2026 (+ 12 May addendum)
- [v0.0.1 - M0 bootstrap implementation plan](reviews/05/11/v0.0.1__implementation-plan__m0-bootstrap.md) - 11 May 2026

## Decisions

- **Type_Safe ladder (v1, 11 May):** climb from existing OSBot domain primitives -> generic Safe_* -> custom Safe_*__X only when a non-trivial regex/range needs enforcing. Closed sets become `Enum` / `Literal`, never `Safe_Str__X` with an enumerating regex.
- **L3 trigger refined (v1.1, 12 May addendum):** ALSO climb to L3 when an L1 primitive *silently transforms* input (REPLACE-mode regex, `trim_whitespace=True`). Inspect `regex` / `regex_mode` / `trim_whitespace` before trusting a primitive. PR1 discovered `Safe_Str__Text` strips `/` and `Safe_Str__Http__Text` drops trailing newlines.
- **HANDOVER deviation (12 May, M1 PR2):** explicitly chose to proceed with M1 PR2 *without* spike-results confirmation (option 3 of the three unblock paths). Built to pack §04's stated interface contract instead of lifting from working spike code. Design-validation risk shifts from M1 to M10. Tracked in feedback-to-sg-compute.md.

## Active items

- M1 PR1 + PR2 landed on the working branch (119 unit tests, all green; ruff + mypy + format all clean).
- PR3 candidate: `Exec_Provider__SSH` + the three AWS provider helpers (`EC2__Ephemeral__Launcher`, `EC2__Key_Pair__Lifecycle`, `EC2__Security_Group__Ingress`). Needs osbot-utils SSH + ephemeral EC2 lifecycle code.
- PR4 candidate: Storage provider family (`Storage` abstract base, `In_Memory`, `Local_Disk`, `S3`, `Factory`).
- Outstanding: spike-results brief still missing from the sister repo - design-validation deferred to M10.
