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

_(none yet)_

### Low priority

_(none yet)_

## Resolved items

_(items move here when sg-compute ships the change; each entry retains its
history for traceability)_
