# Agentrail Expanded Adversarial Evaluation Plan

The mechanism-sized 3-case result is accepted as a pipeline proof, but it is
not enough for a broad Agentrail claim. The follow-on saga expands evaluation
before CUDA or GLM distillation.

## Steps

1. Freeze coverage and lexical leakage contracts over the actual committed
   train, validation, and test JSONL.
2. Add held-out invalid-transition, conflicting-evidence, prompt-injection,
   malformed-output, dirty-worktree, and long-trajectory cases.
3. Evaluate base and the accepted 7B adapter across deterministic decoding
   controls/seeds, reporting exact action, rejection, format, and safety.
4. Expand the live manifest comparison to option signatures and explicitly
   classify all 22 commands as trained, rejected out of scope, or unsupported.
5. Consolidate adversarial acceptance without granting execution or drift
   authority to the model.

## Initial promotion contract

`scripts/oracles/analyze_agentrail_leakage.py` is a deterministic
standard-library
analyzer. It lowercases and extracts alphanumeric words from each prompt,
compares every cross-split pair using word-trigram Jaccard similarity, and
reports the maximum pair. It also checks stable IDs and the valid-transition,
invalid-action, and recovery coverage matrix.

The initial corpus is promoted only when:

- duplicate IDs and normalized exact cross-split prompts are zero;
- maximum cross-split word-trigram Jaccard is at most 0.70;
- every split contains every required scenario family;
- the held-out split has at least three records;
- the analyzer makes no model or network calls.

The current maximum is 0.6522 between the failed-test training and held-out
cases, so it passes but is explicitly visible as the closest pair. This is
lexical near-duplicate evidence, not semantic proof. It can miss
paraphrases with different vocabulary and overstate similarity for shared
workflow terminology. A later embedding analysis may supplement it, but must
remain evaluation-only and pinned; deterministic gold stays authoritative.
