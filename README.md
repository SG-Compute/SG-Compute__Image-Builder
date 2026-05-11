# SG-Compute Image Builder (`sgi`)

A CLI for producing ephemeral EC2 images by capturing the state of a working
instance and replaying it onto a fresh one. **The image-building layer** for
sg-compute; the package manager is the next layer up and out of scope here.

- **CLI binary:** `sgi`
- **Python package:** `sg_image_builder`
- **Current version:** `v0.0.1` (pre-release; first tagged release will be `v0.1.0`)

## The headline

`sg lc create` (local-claude) currently takes ~10 minutes cold-start. Custom
AMIs take ~30 minutes to bake and load even slower because of EBS lazy-load.
`sgi` does the slow work once on a build instance, captures the result as
files in Storage, and replays it onto fresh instances at NIC line rate.

**Target cold-start:** ~600s → ≤90s (p50) for the local-claude path.

## The seven verbs

| Verb | What it does |
|---|---|
| `capture` | Observe a real installation on a build host; record what changed |
| `package` | Turn a capture into a versioned bundle (tar.zst + manifest + sidecar) |
| `publish` | Upload a bundle to Storage at its IFD-versioned path |
| `load` | Pull a bundle from Storage onto a target; replay file changes |
| `strip` | Remove files not required by the spec's test suite |
| `test` | Run a spec's end-to-end test suite against a target |
| `benchmark` | Measure first-load, boot, execution (three canonical moments) |

Plus thin verb groups: `recipe`, `spec`, `instance`, `storage`, `events`,
`shell`, `connect`, `init`, `version`, `doctor`.

## Status

Bootstrap (**M0**) is in place: package skeleton, CI, agentic team scaffold,
and `sgi --version` work. Provider foundations and the rest of the milestones
follow per the implementation plan. The authoritative brief pack lives in
`library/dev_packs/v0.2.8__sg-image-builder/` in the sister repo
`the-cyber-boardroom/SGraph-AI__Service__Playwright` (branch
`claude/review-project-debrief-dN7dO`).

## Quick start

```bash
git clone https://github.com/SG-Compute/SG-Compute__Image-Builder.git
cd SG-Compute__Image-Builder

python -m venv .venv && source .venv/bin/activate
pip install -e .[test]

sgi --version
```

## Working with workspaces

sgi state lives in workspace folders. The convention in this repo is to put
them under `_vaults/`, which is gitignored so workspace contents never get
committed.

To start a new workspace:

    cd _vaults
    mkdir my-experiment
    cd my-experiment
    sgi init

To version-control a workspace independently (recommended):

    sgit init my-workspace
    cd my-workspace
    sgi init
    # ...do work...
    sgit commit "captured vllm-disk baseline"
    sgit push

sgi never invokes `sgit` (principle P14). Vault use is the user's choice.

## Repository layout

```
SG-Compute__Image-Builder/
├── sg_image_builder/                 # the package (sgi)
├── sg_image_builder__tests/          # parallel test tree (unit/integration/e2e)
├── sg_image_builder_specs/           # per-spec definitions (9 specs)
├── scripts/                          # build helpers (zipapp)
├── docs/                             # user-facing documentation
├── humans/dinis_cruz/                # human briefs and debriefs
├── team/roles/                       # agentic team workspaces
├── _vaults/                          # workspace container (gitignored)
└── .github/workflows/                # CI: pr.yml, main.yml, tag.yml
```

## Principles

Twenty-one principles govern every design decision; the seven that matter
most day-to-day:

1. **Storage abstracted** — never `s3.*` in service code
2. **Capture, don't construct** — observe a real install, don't write installers
3. **Tests are the contract** — strip removes anything tests don't require
4. **IFD versioning** — paths are immutable; updates publish new paths
5. **Workspace folder is the unit of context** — no global state, no hidden files
6. **Cloud-agnostic** — no AWS-specific code in core; AWS lives behind providers
7. **Offline-first** — every operation works without internet given a local Storage

See `docs/principles.md` for the full list of 21 (mirrored from the dev pack).

## License

Apache License 2.0 — see [LICENSE](LICENSE).
