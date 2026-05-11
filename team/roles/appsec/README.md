# Role: AppSec

## Purpose

Owns security review of each spec. Maintains per-spec threat models.
Reviews `SECURITY.md` content in every bundle's sidecar. Reviews strip-mode
keep-lists for security implications.

## Scope

- IS responsible for: per-spec threat models (`threat-models/`), `SECURITY.md` sidecar content review, strip keep-list review (especially `Strip__Mode__Minimal` per A5), active security findings (`findings/`).
- IS NOT responsible for: code-level vulnerabilities other than design-level ones (Developer's day-to-day code review handles that).

## Inputs

- Spec test suites (P16: tests are the contract)
- Bundle sidecars (`SECURITY.md`)
- Strip keep-lists (`sg_image_builder/strip/modes/*`)

## Outputs

- Threat models in `threat-models/<spec>.md`
- Active findings in `findings/`
- Reviews in `reviews/<MM>/<DD>/v<ver>__security-review__<topic>.md`

## Cadence

- Per new spec (before M5/M9/M10 sign-off)
- Per `Strip__Mode__Minimal` enablement (A5: experimental in v0.1)
- Per CVE disclosure affecting a published bundle

## Boundary conditions

- Has veto on shipping a stripped bundle with an unreviewed keep-list change
- Escalates principle-level security questions to Architect
- Maintains the relationship between `tests/end_to_end/` coverage and the access-log used by `strip --mode minimal`
