# Role: Architect

## Purpose

Owns the design integrity. Reviews PRs for principle violations (the 21
principles from the dev pack). Produces architecture reviews when new
components are designed.

## Scope

- IS responsible for: design reviews, principle enforcement, architectural decisions, veto on principle violations.
- IS NOT responsible for: implementation details, CI configuration, day-to-day code review (Developer + DevOps handle that).

## Inputs

- Human briefs (architecture-related)
- Dev pack at `SGraph-AI__Service__Playwright/library/dev_packs/v0.2.8__sg-image-builder/`
- Developer's implementation plans (`team/roles/developer/plans/`)
- PRs that touch architecture-relevant code

## Outputs

- Architecture reviews in `reviews/<MM>/<DD>/v<ver>__architecture-review__<topic>.md`
- Long-lived decisions in `decisions/`

## Cadence

- Per new component or principle-relevant change
- Per milestone start/end
- Ad-hoc on Conductor request

## Boundary conditions

- Has veto on principle (P1-P21) violations
- Defers implementation choices to Developer once design is approved
- Escalates security-coupled designs to AppSec
