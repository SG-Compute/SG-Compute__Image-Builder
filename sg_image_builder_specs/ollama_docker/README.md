# Spec: `ollama_docker`

Ollama running inside a Docker container.

- **Instance:** `c5.xlarge` on `al2023`
- **Lands in:** M9 (CPU specs)
- **Primitive proved:** bundles can contain Docker images (captured via `docker save`); the load restores the image's overlay2 directory; Docker picks it up natively.

## Bundles

1. `docker-daemon` (reused from spec 5)
2. `ollama-docker-image` — `docker save ollama/ollama:latest -o image.tar`, ~1 GB
3. `ollama-gemma-2b` (reused from spec 6)

## Tests "works" by

Same shape as `ollama_disk` - `curl` to `localhost:11434` - but the test
should verify the service is running *inside Docker*, not natively.

Full design lives in the dev pack §08.
