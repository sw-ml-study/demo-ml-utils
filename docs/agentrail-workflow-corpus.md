# Frozen Agentrail Workflow Corpus

The Stage 2 training corpus is a small, provenance-tracked teaching fixture,
not a scrape of an installed command's help text. MLPL generates the committed
files under `fixtures/training/agentrail-workflow/` from
`src/training/agentrail_workflow_corpus.mlpl`.

## Contents

The 6/3/3 train, validation, and held-out splits contain MLX-LM
prompt/completion records from three scenario families:

- valid transitions among `next`, `begin`, and `complete`;
- invalid proposals that must be rejected and replaced by a safe action;
- recovery cases covering failed tests, dirty worktrees, completion metadata,
  and the mandatory post-completion stop.

Each completion has an explicit `ACTION` and `REASON`. IDs and scenario text
are distinct across splits. The corpus is deliberately small: it establishes
the schema, safeguards, projection, and evaluation seam for the 7B demo; it is
not evidence of broad Agentrail competence by itself.

## Licensing and provenance

Every record is deterministically written for this MIT-licensed repository.
`provenance.json` records the copyright, MIT dataset license, generation
method, redistributability, and zero private, teacher, or live-help examples.
No external conversation or repository source is copied into the corpus.

`manifest.json` freezes the three command names and states that it is a
repository-authored training contract. It is intentionally not captured from
the currently installed `agentrail --help`. A later evaluation step captures
live help separately and reports drift; live output cannot silently become
training data.

## Reproducibility and validation

The default gate regenerates the corpus into ignored `tmp/`, checks schema,
family counts, exclusions, frozen commands, and leakage declarations, then
compares all five outputs byte-for-byte with the committed fixtures. This
detects generator or projection drift before opt-in model training.

The deterministic validator remains the workflow authority. Model output can
propose or explain an action but cannot update Agentrail state automatically.
