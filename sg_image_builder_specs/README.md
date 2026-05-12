# sg_image_builder_specs/

Per-spec packages — the v1 spec ladder. Each subdirectory is (will become) a
separately-installable Python package owning its manifest, recipe, and test
suite. The test suite is the contract (principle P16).

## Ladder (CPU-first → GPU last)

| # | Spec              | Instance     | Lands in milestone | Tests "works" by |
|---|-------------------|--------------|--------------------|------------------|
| 1 | `ssh_file_server` | t3.micro     | M5                 | SSH in, create/read/delete a file |
| 2 | `python_server`   | t3.micro     | M9                 | HTTP server returns hello-world |
| 3 | `node_server`     | t3.micro     | M9                 | Same, Node.js |
| 4 | `graphviz`        | t3.micro     | M9                 | `.dot` in, PNG out |
| 5 | `docker`          | t3.small     | M9                 | `docker run hello-world` works |
| 6 | `ollama_disk`     | c5.xlarge    | M9                 | Ollama binary + model on disk, `/api/generate` responds |
| 7 | `ollama_docker`   | c5.xlarge    | M9                 | Same in a container |
| 8 | `vllm_disk`       | g5.xlarge    | M10                | vLLM serving with the working flag set |
| 9 | `vllm_docker`     | g5.xlarge    | M10                | Current local-claude path, just fast |
| L1 | `ollama_mac_container` | Mac M-series (local) | M9 (local dev) | Container calls host Ollama via host-gateway; `curl` from inside container returns tags + completion |

## Per-spec layout (target shape, per dev pack §08)

```
sg_image_builder_specs/<spec>/
├── pyproject.toml          # separately-installable package
├── README.md
├── manifest.py             # Schema__Spec definition
├── recipes/
│   ├── default.json
│   └── minimal.json        # stripped variant
├── tests/
│   ├── unit/
│   ├── integration/
│   └── end_to_end/
└── version
```

In M0 these directories ship as **README-only stubs**. Real content lands
spec-by-spec in M5 (`ssh_file_server`), then M9, then M10.
