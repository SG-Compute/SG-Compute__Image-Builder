# Spec: `ssh_file_server`

**The hello-world of sgi.** Proves the entire workflow end-to-end.

- **Instance:** `t3.micro` on `al2023`
- **Lands in:** M5 (first integration milestone)
- **Recipe:** empty steps - AL2023 already ships SSH and the basic tools
- **Tests "works" by:** SSH in, create/read/delete a file

## What it produces

An EC2 instance you can SSH into. No additional service, no extra software.

## KPI targets

| Moment       | p50          |
|--------------|--------------|
| `first_load` |  5,000 ms    |
| `boot`       | 25,000 ms    |
| `execution`  |    100 ms    |
| `cold_start` | 45,000 ms    |

## Why it's spec #1

If sgi can't ship this, it can't ship anything. This is the smoke test for
every part of the workflow. Once it works on real AWS, the rest of the specs
are variations.

Full design lives in the dev pack §08.
