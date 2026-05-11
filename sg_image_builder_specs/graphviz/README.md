# Spec: `graphviz`

A stateless single-action target: take a `.dot` file in, produce a PNG out.

- **Instance:** `t3.micro` on `al2023`
- **Lands in:** M9 (CPU specs)
- **Primitive proved:** a spec doesn't need a long-running service. Also the first spec where `strip --mode minimal` is genuinely aggressive.

## Bundles

1. `graphviz-runtime` — the `graphviz` package and its libraries, captured from `apt-get install graphviz`

## Tests "works" by

- `dot -Tpng /tmp/in.dot > /tmp/out.png` produces a PNG (verified via `file`)

Full design lives in the dev pack §08.
