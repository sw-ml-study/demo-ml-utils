# Agentrail Adversarial Held-Out Cases

The expanded suite commits 12 evaluation-only cases under
`fixtures/evaluation/agentrail-adversarial/`, with two examples in each family:
invalid transitions, conflicting evidence, prompt injection, malformed model
output, dirty worktrees, and longer trajectories.

Every record has a stable ID, prompt, exact expected action, rejection label,
and explicit zero automatic-send/execute fields. Provenance declares MIT,
repository-authored synthetic material with zero training, private, live-help,
or model-generated examples. These records must never be appended to the MLX
train or validation files.

The deterministic validator checks schema, exact family counts, ID uniqueness,
zero overlap with all existing corpus split IDs, safety flags, provenance, and
maximum word-trigram similarity against every training/validation/original-test
prompt. Promotion requires similarity at most 0.70. This is still lexical—not
semantic—separation evidence.

Expected actions deliberately go beyond the original three exact commands:
they include requests for authoritative state or scope clarification, rejection
of injected/malformed actions, preservation of unrelated changes, correction
of the earliest failed check, and the post-completion metadata/stop boundary.
The next step scores the base and accepted 7B adapter without training on these
answers.
