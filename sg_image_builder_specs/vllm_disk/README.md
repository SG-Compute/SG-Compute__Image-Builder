# Spec: `vllm_disk`

vLLM running natively. **First GPU spec.**

- **Instance:** `g5.xlarge` on `al2023` (DLAMI base for GPU drivers)
- **Lands in:** M10 (GPU specs)
- **Primitive proved:** GPU instance; same capture/load workflow as CPU specs; largest bundle sgi has ever handled (~15 GB weights).

## Bundles

1. `nvidia-driver-os-bundle` — captured from DLAMI base (may be empty if we start from DLAMI)
2. `cuda-runtime` — CUDA libraries
3. `vllm-runtime` — vLLM Python package and its deps
4. `qwen3-coder` — the model weights, ~15 GB

## Architectural decision

We start from the DLAMI AL2023 OSS variant for GPU specs. Trade-off:
drivers always work; cost is ~20s of boot time per launch.

## Tests "works" by

- `nvidia-smi` returns `A10G`
- `curl http://localhost:8000/v1/models` returns 200 with `qwen` in the output
- `curl http://localhost:8000/v1/completions` produces a non-empty completion

Full design lives in the dev pack §08.
