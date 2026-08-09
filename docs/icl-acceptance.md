# ICL Acceptance Report

`just icl-acceptance` closes the bounded in-context-learning saga. It rebuilds
the comparison IR twice and requires byte-identical tagged JSON, exact few-shot
predictions, identical deployment fingerprints, and zero parameter updates
across the learner and causal-control report.

The consolidated adversarial gate rejects malformed and non-finite source data,
duplicate context IDs, context/query leakage, invalid IR versions and alignment,
and exhausted context, association-work, evidence, output, and atomic byte
budgets. Atomic publication validates before replacement, verifies exact bytes
and parsed semantics after read-back, and preserves an existing destination
when a pre-write budget check fails.

Native code supplies bounded I/O, numeric arrays, tagged JSON, and atomic file
replacement. MLPL owns the record and leakage policy, frozen associative
mechanism, causal controls, metrics, IR normalization, budgets, and semantic
acceptance.

No external model is required by the default gate. Optional pinned-provider or
local-model corroboration may be added later, but it is explicitly not the
acceptance authority because model versions, tokenization, sampling, and service
behavior introduce different variables from this deterministic mechanism.

This acceptance does not establish transformer behavior, prompt portability,
large-model quality, privacy, provider reproducibility, or statistical
generalization. It establishes that this tiny bounded mechanism changes outputs
from context while deployment parameters remain unchanged and evidence is
published fail-closed.
