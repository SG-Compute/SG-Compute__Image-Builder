# Developer — Master Index

_Maintained by the Developer role with help from the Librarian._

## Latest reviews

- [v0.0.1 - M0 bootstrap implementation plan](reviews/05/11/v0.0.1__implementation-plan__m0-bootstrap.md) - 11 May 2026
- [v0.0.1 - Type_Safe usage calibration](reviews/05/11/v0.0.1__type-safe-usage-calibration.md) - 11 May 2026

## Decisions

- **Type_Safe ladder:** climb from existing OSBot domain primitives -> generic Safe_* -> custom Safe_*__X only when a non-trivial regex/range needs enforcing. Closed sets become `Enum` / `Literal`, never `Safe_Str__X` with an enumerating regex. (calibration review above)

## Active items

- M1 schemas will use the calibrated rule. First M1 PR introduces `sg_image_builder/types/` and `sg_image_builder/schemas/` per the mapping in the calibration review.
