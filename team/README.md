# team/

Agentic team workspace for `SG-Compute__Image-Builder`. Pattern lifted from
`SG_Send__Deploy`. Each role's `roles/<role>/` is a self-contained
workspace.

## Roles

| Role        | Owns                                                                     |
|-------------|--------------------------------------------------------------------------|
| Conductor   | Coordinates the team; routes briefs; summarises outcomes                 |
| Architect   | Design integrity; veto on principle (P1-P21) violations                  |
| Developer   | Writes the code; produces per-milestone implementation plans             |
| DevOps      | CI/CD, secrets, release pipeline, observability                          |
| AppSec      | Per-spec threat models; `SECURITY.md` reviews; strip keep-list review    |
| Librarian   | Indexes, naming conventions, cross-linking, master indexes               |

See each role's `README.md` for scope, inputs, outputs, cadence, and
boundary conditions.

## Conventions

- **Reviews** live under `<role>/reviews/<MM>/<DD>/v<ver>__<type>__<slug>.md`
  (month/day folders, no year — matches the dev pack convention)
- **Naming:** `v<version>__<type>__<topic-slug>.md`
- **Master indexes:** maintained by the Librarian on each merge

The structure is intentionally low-tech: folders and markdown.
Grep-able, git-blameable, survives any tooling change.
