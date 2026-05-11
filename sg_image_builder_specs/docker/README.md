# Spec: `docker`

Docker daemon working on AL2023. Foundation for subsequent container-based
specs (`ollama_docker`, `vllm_docker`).

- **Instance:** `t3.small` on `al2023`
- **Lands in:** M9 (CPU specs)
- **Primitive proved:** the bundle includes a daemon (more complex than a simple service). Capture preserves `/etc/docker/`, `/var/lib/docker/` initial state, and the systemd unit.

## Bundles

1. `docker-daemon` — Docker CE + containerd + cli, captured from `dnf install docker`

## Tests "works" by

- `sudo docker run --rm hello-world` prints `Hello from Docker`

Full design lives in the dev pack §08.
