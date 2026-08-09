# Model Visualization

Build a renderer-neutral, budgeted visualization handoff over accepted Safetensors and GGUF catalogs and summaries. MLPL owns schema construction, provenance, layout inputs, tile derivation, and budget validation; renderers and transport remain explicit consumers.

1. Define a versioned scene/tile IR with stable IDs, provenance, object/payload budgets, golden JSON, and headless validation.
2. Build deterministic tensor-city model/layer layouts from bounded catalogs.
3. Add selected-tensor distribution and sampled-surface tiles from bounded statistics.
4. Add quantization-block and before/after error tiles with explicit LOD budgets.
5. Add CLI/server transport and an optional 3D client while retaining headless snapshots and complete the acceptance report.

Acceptance: visualization consumes derived bounded summaries rather than complete raw tensors; every LOD validates object and payload budgets; default demos are self-describing and headlessly testable without a browser.