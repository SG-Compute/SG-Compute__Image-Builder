# Feedback for sg-compute team

This file accumulates suggestions for the sg-compute team based on sgi's
experience consuming `sg lc *` via shell-out (`Exec_Provider__Sg_Compute`).

Items get added every time `Exec_Provider__Sg_Compute` has to fall back to
text parsing because `sg lc` lacks a structured-output flag. Reviewed
periodically and prioritised by impact.

## Open items

### High priority

#### `sg lc list --json` should output structured JSON

- **Why:** sgi shells out to this and currently parses table output.
- **Impact:** brittle; breaks when sg-compute's table format changes.
- **Proposed shape:**
  ```json
  [
    {
      "name":          "compute-1",
      "instance_id":   "i-xxx",
      "state":         "running",
      "region":        "eu-west-2",
      "instance_type": "g5.xlarge"
    }
  ]
  ```
- **First observed:** anticipated during M2 (workspace + CLI bootstrap)
- **Status:** to confirm once `Exec_Provider__Sg_Compute` lands in M1

#### `sg lc exec --json` should wrap stdout/stderr/exit_code

- **Why:** `Exec_Provider__Sg_Compute.exec_command()` needs structured output to populate `Schema__Exec__Result`.
- **Impact:** without this, every command result requires bespoke parsing.
- **Proposed shape:**
  ```json
  {
    "command":    "uname -a",
    "stdout":     "Linux ...",
    "stderr":     "",
    "exit_code":  0,
    "elapsed_ms": 142
  }
  ```
- **First observed:** anticipated during M1 (`Exec_Provider__Sg_Compute` implementation)

### Medium priority

#### `v0.2.8__sgi-spike-results.md` is missing from the sister repo

- **Why:** The HANDOVER (`library/dev_packs/v0.2.8__sg-image-builder/HANDOVER.md` in the sister repo) gates **M1+** on the spike's decision-gate (`strong pass` / `conditional pass` / `fail`). The results brief is supposed to land at `team/comms/briefs/v0.2.8__sgi-spike-results.md` in the sister repo.
- **Status as of 12 May 2026:** the spike brief itself still reads `Status: PROPOSED - ready to start` and no `sgi-spike-results.md` exists on the branch I have read access to (`claude/review-project-debrief-dN7dO`).
- **Decision taken:** Dinis chose to proceed with M1 PR2 anyway (option 3 of the three unblock paths: scratch-build against the pack's interface contract, accept the design-validation risk shifting to M10).
- **What needs to happen eventually:** run the spike per `v0.2.8__sgi-local-claude-validation-spike.md`, publish the results brief, then retro-validate the calibrated types + exec flow in this repo against what the spike actually used. If results land in the `≤ 240 s` range, the PR2 design holds. If they don't, M1 work needs revision before more code lands.
- **Tracked at:** `team/roles/developer/reviews/05/12/v0.0.1__m1-pr2__exec-providers.md` §"HANDOVER deviation"

#### Dev pack §10 over-prescribes custom `Safe_Str__*` subclasses

- **Why:** The pack's instinct (and the original brief) is to spawn a
  `Safe_Str__Foo` per domain concept (Image_Id, Provider_Name, Spec_Id,
  Layer_Name, ...). The Type_Safe canon (see refs below) says the rule
  is *ban raw primitives*, not *invent a subclass per noun*.
- **Symptom:** Reading the brief gives the impression that every string
  field must be its own `Safe_Str__X`. In practice, OSBot-Utils already
  ships 100+ domain primitives (`Safe_Str__Url`, `Safe_Str__File__Path`,
  `Safe_Str__Slug`, `Safe_Str__Version`, `Safe_Str__Id`, `Safe_Id`, ...)
  and the **generic** `Safe_Str` is the right answer when no extra
  validation is needed.
- **Proposed amendment to §10:** adopt the four-level ladder documented
  in `team/roles/developer/reviews/05/11/v0.0.1__type-safe-usage-calibration.md`:
  1. `bool` for booleans
  2. **Existing OSBot domain primitive** when one fits
  3. Generic `Safe_Str` / `Safe_Int` / `Safe_UInt` / `Safe_Float` when no domain primitive fits
  4. Custom `Safe_Str__X` subclass **only** when a non-trivial regex /
     length / range needs enforcing AND a failing test exists for the boundary
- **Closed-set values** (e.g. provider name, exit code, build mode) should be
  `Enum` (or `Literal` for very small sets), NOT a `Safe_Str__X` with an
  enumerating regex.
- **Reference docs (cloned read-only):** `library/dependencies/osbot-utils/type_safe/` in `the-cyber-boardroom/SGraph-AI__App__Send` (v3.63.4 `for_llms__type_safe.md`, v3.28.0 `for_llms__osbot-utils-safe-primitives.md`)
- **First observed:** pre-M1 review, 11 May 2026
- **Status:** sgi will follow the calibrated rule from M1 onwards; flagging
  back so the pack can decide whether to make this the default for other
  consuming projects

### Low priority

_(none yet)_

## Resolved items

_(items move here when sg-compute ships the change; each entry retains its
history for traceability)_
