# docs/

User-facing documentation for sgi. Stays light during the bootstrap phase
and fills out spec-by-spec as the implementation progresses.

## Authoritative reference

The full design pack (21 principles, 9 specs, the architecture, CLI surface,
strip workflow, etc.) lives at:

- Sister repo: `the-cyber-boardroom/SGraph-AI__Service__Playwright`
- Branch: `claude/review-project-debrief-dN7dO`
- Path: `library/dev_packs/v0.2.8__sg-image-builder/`

Read order for new contributors:

1. The pack's `README.md`
2. `00__pack-overview/quick-reference.md`
3. `01__principles/principles.md`
4. `02__architecture/architecture.md`
5. `09__implementation-plan/implementation-plan.md`

And the `HANDOVER.md` at the pack root — it carries the Architect review
(D1-D5) and concerns (A1-A9) that overlay the pack.

## What lives here

| Path                | What                                                   |
|---------------------|--------------------------------------------------------|
| `README.md`         | This file                                              |
| `principles.md`     | _(future)_ Mirror of the 21 principles                 |
| `cli-surface.md`    | _(future)_ Mirror of pack §03 once CLI stabilises      |
| `kibana-dashboards/`| _(future)_ Importable JSON dashboards (M11)            |

## What does NOT live here

- Per-spec docs - those live with each spec under `sg_image_builder_specs/<spec>/`
- Bundle sidecars (`SKILL.md`, `USAGE.md`, `SECURITY.md`) - those live in the bundle's `sidecar.zip`
- Briefs and debriefs - those live under `humans/dinis_cruz/`
- Team reviews - those live under `team/roles/<role>/reviews/`
