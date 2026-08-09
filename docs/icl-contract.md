# In-Context Learning Record Contract

`just icl-contract` builds `sw-ml-study.icl-record` version 1 from the shared
fixture. Context IDs `201`–`202` and query IDs `301`–`303` remain disjoint under
six explicit comparisons plus full source-split validation.

The deployment model stays frozen at `[0,0,0]`; its canonical fingerprint is
identical before and after inference and updates remain zero. The zero-shot
baseline ignores context labels, predicts `[0,0,0]`, and has held-out MSE 65.
This creates an honest reference for associative ICL rather than claiming that
record construction performs learning.

MLPL owns schema/split validation, leakage work, record construction, baseline
inference/loss, mode semantics, fingerprints, budgets, and deterministic tagged
JSON. Native code supplies bounded reads and generic JSON. This teaching record
is not a transformer prompt format, tokenizer, production API, or proof that
context improves predictions.
