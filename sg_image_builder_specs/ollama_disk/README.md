# Spec: `ollama_disk`

Ollama binary running natively on disk (no container). Model weights on
disk too. **The first multi-bundle recipe; first big bundle (~1.6 GB).**

- **Instance:** `c5.xlarge` on `al2023`
- **Lands in:** M9 (CPU specs)
- **Primitive proved:** multi-bundle recipes work; large bundles work; "model as separate IFD artefact" pattern works (update runtime without re-uploading the model)

## Bundles

1. `ollama-runtime` — Ollama binary, captured from `curl -fsSL https://ollama.com/install.sh | sh`
2. `ollama-gemma-2b` — gemma2:2b model weights (~1.6 GB)

## Tests "works" by

- `curl http://localhost:11434/api/tags` lists `gemma2:2b`
- `curl http://localhost:11434/api/generate` produces a non-empty response

Full design lives in the dev pack §08.
