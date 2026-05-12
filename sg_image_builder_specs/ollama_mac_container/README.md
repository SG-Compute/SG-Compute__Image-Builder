# Spec: `ollama_mac_container`

A container application layer talking to Ollama running natively on the Mac
host. Mirrors the local-claude pattern (`vllm_docker`) for local Mac
development on Apple Silicon.

- **Platform:** macOS (Apple Silicon M5 / ARM64), local-only (not AWS)
- **Ollama:** runs on the **host** (native, with Metal / ANE / Apple GPU access) — NOT inside the container
- **Primitive proved:** a container can reach Ollama at `http://host.docker.internal:11434` via host-gateway networking; the application layer is fully containerised while the inference engine stays on the host for GPU access.

## Bundles

This spec does not use the cloud capture/restore workflow. Instead the
"bundle" is a portable `Dockerfile` + startup script that can be pointed at
any host-provided Ollama endpoint.

1. `ollama-host` — Ollama installed and running on the Mac host via
   `brew install ollama` (or `curl -fsSL https://ollama.com/install.sh | sh`).
   Model pulled with `ollama pull gemma2:2b`.
2. `app-container` — a minimal Python (or Node) service `Dockerfile` that
   calls `http://host.docker.internal:11434`. Built locally with
   `docker build` (Docker Desktop) or `swift run container build`
   (Apple Containers).

## Container runtime options

| Runtime | CLI | Networking to host | Cold start | Notes |
|---------|-----|--------------------|------------|-------|
| **Docker Desktop** | `docker run` | `--add-host host.docker.internal:host-gateway` (auto on Mac) | moderate | Well-tested; runs in a Linux VM; `--network host` is NOT supported natively on macOS |
| **Apple Containers** | `swift run container run` | direct host networking, no extra flag needed | fast (native ARM64) | Very new (2025); no Linux VM overhead; `host.docker.internal` alias may need manual setup |

Both runtimes resolve `host.docker.internal` inside the container to the Mac
host IP. Docker Desktop injects this automatically; Apple Containers may
require passing `--add-host host.docker.internal:host-gateway` or setting
the env var `OLLAMA_HOST` to the host's IP directly.

## Tests "works" by

- `curl http://host.docker.internal:11434/api/tags` issued **from inside the container** lists `gemma2:2b`
- A `/api/generate` call from inside the container returns a non-empty completion

These two checks prove: host-gateway networking is wired correctly AND the
container can drive an inference request end-to-end against host Ollama.

## Notes

Ollama must be running on the host before starting the container:

```bash
# Host — start Ollama (if not already running as a service)
ollama serve &
ollama pull gemma2:2b

# Docker Desktop
docker run --rm \
  --add-host host.docker.internal:host-gateway \
  -e OLLAMA_BASE_URL=http://host.docker.internal:11434 \
  app-container \
  curl http://host.docker.internal:11434/api/tags

# Apple Containers (equivalent)
swift run container run \
  -e OLLAMA_BASE_URL=http://host.docker.internal:11434 \
  app-container \
  curl http://host.docker.internal:11434/api/tags
```

Full design lives in the dev pack §08.
