# Qwen2.5-Coder 7B Agentrail QLoRA Demo

`just agentrail-coding-model` is the opt-in Stage 2 demonstration. It trains
four LoRA-injected layers of the local 4-bit Qwen2.5-Coder-7B-Instruct model on
the frozen, MIT-provenance Agentrail workflow corpus. `just
agentrail-coding-model-eval` reloads the ignored adapter and repeats held-out
base-versus-adapted generation without retraining.

## Demonstrated problem

The base coding model can describe plausible work but does not reliably emit
the frozen workflow action. The held-out cases require three different kinds
of behavior:

1. begin a reviewed pending step with exactly `agentrail begin`;
2. reject premature completion after a failed test and prescribe the scoped
   repair;
3. emit `STOP` after completion metadata is committed.

The evaluator applies Qwen's actual chat template, greedily generates a bounded
response, extracts the first `ACTION` line, and separately scores exact action
text and rejection classification. Model output is never executed.

## Accepted run

The accepted configuration uses the 12/3/3 corpus, batch size 1, 80 Adam
iterations at `5e-5`, four trainable transformer layers, rank 8, prompt masking,
gradient checkpointing, maximum sequence length 256, and seed 23.

| Evidence | Base/start | Adapted/final |
|---|---:|---:|
| Validation loss | 4.297 | 0.798 |
| Held-out exact actions | 0 / 3 | 3 / 3 |
| Held-out rejection classification | 2 / 3 | 3 / 3 |
| Test loss / perplexity | — | 1.098 / 2.997 |
| Trainable parameters | — | 2.884M of 7,615.617M (0.038%) |
| MLX training peak | — | 4.781 GB |

The fresh-loaded adapter is 11,540,338 bytes with SHA-256
`e34378b6483ddf3e425b7e7b75726eba345170f7850e40d10133a85082923372`.
Evaluation peak was 4.537 GB. Both are comfortably below the 12.288 GB
acceptance ceiling.

An earlier 80-step trial on only six training records was rejected at 1/3
exact actions. Expanding deterministic failed-test, commit, dirty-tree, and
stop coverage produced 2/3 at 60 conservative steps; extending the still-
improving schedule to 80 produced 3/3. These failed trials are important:
training loss alone did not satisfy acceptance.

## What this does not prove

Three held-out examples are mechanism evidence, not broad Agentrail mastery.
The demo does not yet cover full command arguments, multi-step planning,
malformed metadata, semantic near-duplicate analysis, adversarial prompts, or
new Agentrail versions. It did not train on installed `agentrail --help`; the
next step captures that output only for deterministic drift comparison.

The adapter proposes actions and reasons. `automatic_execute` is zero, and no
model result may edit files, mutate Agentrail state, commit, or send context
without a separate deterministic controller or human authorization.
