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

Status: complete. Bounded range I/O,
`file_size`, budgeted JSON decoding, duplicate-key rejection, and deterministic
record enumeration are shipped and covered by the repository gate.

1. Carry forward the completed range-reader conformance and adversarial
   EOF/overflow evidence.
2. Selective tensor slice reads and initial U8/I8/U16/I16 decoding — runnable
   in the default gate.
3. Mergeable statistics with fixed chunk size — runnable in the default gate.
4. Sparse large-artifact acceptance and measured peak memory — opt-in and
   passing on supported platforms.
5. Versioned, budgeted JSON visualization-summary IR and headless validation —
   runnable without a renderer dependency.

## Saga 3 — `gguf-inspection`

Status: acceptance complete. Bounded GGUF v3 scalar metadata and multiple-tensor cataloging
are runnable over tiny generated fixtures; exact-name selective I8/I16 payload
decoding and one-block Q8_0 golden dequantization are also runnable while
unsupported types remain catalog-visible. See the
[GGUF acceptance report](gguf-acceptance-report.md) for the gate evidence.

1. GGUF header, metadata, tensor directory, and alignment fixtures/parser.
2. Multiple-tensor cataloging, scalar metadata coverage, and catalog-visible
   active tensor type IDs — runnable without payload reads.
3. Unquantized selective I8/I16 tensor decoding — runnable in the default gate.
4. Q8_0 golden block decode and ggml reference parity — runnable in the default gate.
5. Bounded tensor sampling/statistics and measured acceptance report — runnable;
   the visualization gate is open.

## Saga 4 — `model-visualization`

Gate: open. Both Safetensors and GGUF now provide bounded catalogs, selective
decode, mergeable summaries, and measured large-artifact evidence suitable for
a budgeted renderer-neutral handoff.

1. Versioned renderer-neutral scene/tile schema and budget validation —
   runnable with cross-format golden JSON and headless validation.
2. Deterministic cross-format tensor-city layout — runnable from bounded
   catalogs without payload reads.
3. Selected-tensor distribution and sampled-surface tiles — runnable for
   bounded Safetensors integer and GGUF Q8_0 selections.
4. Q8_0 quantization-block and before/after error tiles — runnable with golden
   pointwise and aggregate metrics.
5. Bounded CLI/server JSONL transport and optional dependency-free client —
   runnable with deterministic envelopes; headless MLPL validation is retained
   as the acceptance authority.

Status: acceptance complete. See the
[visualization acceptance report](visualization-acceptance-report.md).

## Saga 5 — `native-quantization-and-conversion`

Gate: open. The Q8_0 reader, reconstruction metrics, error IR, and bounded
transport now provide reusable golden evidence for encoder work.

1. Numeric conversion/error metric golden vectors — runnable with bounded
   saturating i8/u8, f64 identity, and deterministic comparison evidence.
2. Symmetric INT8 and Q8_0 encode/decode round trips — runnable with exact
   bytes, independent existing-decoder acceptance, and reconstruction metrics.
3. Simple Q4 encode/decode round trips — runnable with an explicit teaching
   layout, exact nibble bytes, size ratio, and reconstruction evidence.
4. Safetensors-to-GGUF writer with self-validation — runnable for one bounded
   rank-one I8/I16 tensor with atomic output and catalog/value read-back.
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
