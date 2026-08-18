# Agentrail Live-Help Drift Evaluation

`just agentrail-help-drift` captures the installed `agentrail --version` and
`agentrail --help` plus every `agentrail <command> --help` under strict byte
budgets, extracts command and option names, and asks MLPL to compare them with
the frozen three-command training slice.
The captured files live only under ignored `tmp/agentrail-live-help/`.

`just agentrail-help-drift-with-model` additionally reruns the saved 7B adapter
on its frozen held-out set after the manifest verdict. That recipe is opt-in
because it requires the ignored local model and adapter. Its output is advisory
and cannot change the deterministic drift result.

On the accepted run, Agentrail reports version 0.1.0, build commit `2f06132`.
The frozen acceptance interface exposes 22 commands. `next`, `begin`, and
`complete` plus their frozen option signatures are classified as trained. The
remaining 19 commands are explicitly rejected as out-of-scope capabilities;
zero trained contracts are unsupported. Their presence does not mean the
adapter was trained to use them.

The default gate uses committed command-name fixtures, including an adversarial
manifest with `complete` removed and a signature with `complete --summary`
removed. MLPL reports either removal as breaking drift. It also rejects
command-count and byte-budget exhaustion.

## Separation from training

The live help output is never copied into `fixtures/training/agentrail-workflow`
and never passed to MLX-LM training. The frozen corpus provenance continues to
state `live_help_examples=0`. The shell owns bounded process capture; MLPL owns
the deterministic comparison. The trained model has `model_authority=0` and
cannot declare an interface compatible merely because it can produce a
plausible explanation.

The comparison checks command presence and the complete frozen option-name
signatures for the three trained commands. It deliberately does not infer
argument semantics, defaults, or behavioral compatibility from help text.
