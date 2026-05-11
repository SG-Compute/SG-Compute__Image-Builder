# Spec: `python_server`

A FastAPI hello-world server, managed by systemd.

- **Instance:** `t3.micro` on `al2023`
- **Lands in:** M9 (CPU specs)
- **Primitive proved:** bundles can include a systemd service wired to start at boot

## Bundles

1. `python-runtime` v0.1.0 — Python 3.12 + pip/venv + FastAPI + uvicorn
2. `hello-server` v0.1.0 — application code + systemd unit + venv contents

## Tests "works" by

- `curl http://localhost:8000/` returns `{"message":"hello"}`
- `systemctl is-active hello-server` returns `active`

Full design lives in the dev pack §08.
