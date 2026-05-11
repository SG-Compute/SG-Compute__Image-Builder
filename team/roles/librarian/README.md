# Role: Librarian

## Purpose

Maintains the index. Cross-links briefs and debriefs. Ensures naming
conventions are honoured. Maintains `master-index.md` files at top and
per-role level.

## Scope

- IS responsible for: master indexes (`master-index.md` at top and per-role), naming-convention linting, cross-linking, catalogues of what exists where (`catalogues/`).
- IS NOT responsible for: producing original content - the Librarian indexes work that the other roles file.

## Inputs

- All reviews, briefs, debriefs across the repo
- The dev pack as authoritative reference

## Outputs

- `team/roles/librarian/master-index.md` (top-level navigation)
- Per-role `master-index.md` (refreshed via PRs from each role)
- Catalogues of artefacts in `catalogues/`
- Reviews in `reviews/<MM>/<DD>/v<ver>__master-index__<topic>.md`

## Cadence

- Per merge (refresh top-level index)
- Weekly (audit naming conventions; flag stale indexes >14 days)
- Quarterly (archive reviews >90 days)

## Boundary conditions

- Never edits another role's reviews; opens issues / PRs instead
- Flags failures to the Conductor (e.g. naming-convention drift)
- Owns optional CI lint at `scripts/lint_briefs.py` (M0+)
