# Spec: `node_server`

Same as `python_server` but with Node.js + Express. Verifies the
capture/load workflow is genuinely language-agnostic (P2 transparency).

- **Instance:** `t3.micro` on `al2023`
- **Lands in:** M9 (CPU specs)
- **Primitive proved:** different package manager (`npm` vs `pip`), different file layouts (`node_modules/` vs `venv/`), same workflow

## Bundles

1. `node-runtime` — Node 20 + npm + global packages
2. `node-hello-server` — application code + node_modules + systemd unit

Full design lives in the dev pack §08.
