# Role: DevOps

## Purpose

Owns CI/CD, secrets, release pipeline, observability. Owns the `Makefile`.
Owns the GitHub Actions workflows.

## Scope

- IS responsible for: `.github/workflows/`, `Makefile`, build scripts under `scripts/`, branch protection, secrets, release artefacts (zipapp), CI observability.
- IS NOT responsible for: code logic (Developer), threat models (AppSec).

## Inputs

- Dev pack §10 (`dev-ops-brief.md`)
- Coverage gates and test layering per dev pack §07
- Release timeline (from human, when stated)

## Outputs

- CI workflows (`pr.yml`, `main.yml`, `tag.yml`)
- Auto-tag logic driven by `sg_image_builder/version`
- Runbooks in `runbooks/` (release process, secret rotation, etc.)
- Reviews in `reviews/<MM>/<DD>/v<ver>__ci-pipeline__<topic>.md`

## Cadence

- Per PR that touches CI or release tooling
- Per release tag
- Ad-hoc on Conductor request

## Boundary conditions

- Owns secret rotation runbook; secrets live in GitHub Actions config, not in code
- Escalates cost-ceiling breaches ($10/day E2E) to Conductor + human
- Cost ceiling for E2E: $10/day average across all workflows (per dev pack §10)
