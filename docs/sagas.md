# AgentRail Saga Queue

Only one saga is active at a time. Later sagas are initialized after the
preceding saga is completed and archived. Steps are independently reviewable;
newly discovered work is inserted with AgentRail commands, never by editing
append-only `.agentrail/` state.

## Saga 1 — `binary-format-foundations`

1. `repository-check-gate` — add thin `just check` delegation, binary selection,
   fixture-generation conventions, and documentation/link/license checks.
2. `capability-probe` — executable probes for current byte I/O, bit operations,
   exact-integer limits, JSON header handling, and Result errors.
3. `safetensors-header-fixtures` — generated valid/truncated/oversized/malformed
   fixtures and a little-endian header-length decoder with golden tests.
4. `safetensors-catalog` — validate header schema, dtype/shape/offset invariants,
   and emit a deterministic tensor catalog for small files.
5. `bounded-range-upstream-contract` — turn measured whole-file limitations
   into a minimal API/security/acceptance contract without editing upstream.
6. `foundation-report` — catalog runnable demos, document complexity and
   limitations, and decide whether Saga 2 is unblocked.

Complete. The bounded arbitrary-name Safetensors catalog, fulfilled upstream
contract, and [foundation report](foundation-report.md) provide the acceptance
evidence and limitations needed for closeout.

## Saga 2 — `bounded-safetensors-analysis`

Status: active. The gate is satisfied: bounded range I/O,
`file_size`, budgeted JSON decoding, duplicate-key rejection, and deterministic
record enumeration are shipped and covered by the repository gate.

1. Carry forward the completed range-reader conformance and adversarial
   EOF/overflow evidence.
2. Selective tensor slice reads and initial U8/I8/U16/I16 decoding — runnable
   in the default gate.
3. Mergeable streaming statistics with fixed chunk size.
4. Sparse large-artifact acceptance and measured peak memory.
5. JSON visualization-summary IR and headless validation.

## Saga 3 — `gguf-inspection`

1. GGUF header, metadata, tensor directory, and alignment fixtures/parser.
2. Catalog-only operation for supported and unsupported tensor types.
3. Unquantized selective tensor decoding.
4. Q8_0 golden block decode and reference parity.
5. Bounded tensor sampling/statistics and acceptance report.

## Saga 4 — `model-visualization`

1. Versioned renderer-neutral scene/tile schema and budget validation.
2. Tensor-city model/layer layout.
3. Selected-tensor distribution and sampled-surface tiles.
4. Quantization-block and before/after error tiles.
5. CLI/server transport and WASM 3D client, with headless snapshots retained.

## Saga 5 — `native-quantization-and-conversion`

1. Numeric conversion/error metric golden vectors.
2. Symmetric INT8 and Q8_0 encode/decode round trips.
3. Simple Q4 encode/decode round trips.
4. Safetensors-to-GGUF writer with self-validation.
5. Explicit external oracle adapters and reproducible comparison report.

## Saga 6 — `restricted-checkpoint-extraction`

Gate: format and threat-model review is complete and resource budgets can be
enforced before allocation.

1. Passive ZIP/pickle opcode inventory and risk report.
2. Budgeted allow-listed primitive stack-machine parser.
3. Tensor metadata/storage-reference recovery with executable constructs
   rejected rather than invoked.
4. Tensor-only Safetensors extraction.
5. Cross-format verification and adversarial security report.

## Cross-saga rules

- Do not modify `../sw-mlpl` inside these sagas.
- Do not download large models in the default validation gate.
- Never hide Python, llama.cpp, Hugging Face, Rust parsing, or rendering behind
  a claim that MLPL performed the substantive operation.
- Close a saga only when its acceptance evidence and known limitations are in
  user-facing documentation and the full repository gate passes.
