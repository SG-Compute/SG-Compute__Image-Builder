# Spec: `vllm_docker`

The current local-claude path: vLLM in a container. **The spec that
vindicates sgi's existence.**

- **Instance:** `g5.xlarge` on `al2023` (DLAMI base for GPU drivers)
- **Lands in:** M10 (GPU specs)
- **Headline KPI:** `cold_start_target_ms: 90_000` (90s, down from ~600s today)

## Bundles

1. `docker-daemon` (reused from spec 5)
2. `nvidia-container-toolkit-runtime` — Docker GPU access
3. `vllm-docker-image` — `docker save vllm/vllm-openai:latest`
4. `qwen3-coder` (reused from `vllm_disk`)

## Tests "works" by

Identical contract to `vllm_disk` - `/v1/models` returns 200, inference works.
The container-vs-disk implementation is transparent to the test (P2).

## Notes

The validation spike in the sister repo `SGraph-AI__Service__Playwright`
already exercised this path (capture, S3 publish, bundle load). The
production `local_claude` artefact gets promoted to `vllm_docker` here.

Full design lives in the dev pack §08.
