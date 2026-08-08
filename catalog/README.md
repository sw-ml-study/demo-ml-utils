# Demo catalog

`demos.tsv` is the machine-readable inventory used by repository validation
and future runners. It has nine tab-separated columns:

| Column | Contract |
|---|---|
| `id` | Stable lowercase identifier |
| `path` | Repository-relative `.mlpl` path under `demos/` or `probes/` |
| `format` | Primary artifact format or protocol |
| `operation` | User-visible utility operation |
| `implementation_layer` | `mlpl`, `mlpl-native`, or `external` |
| `memory_bound` | `whole-file`, `chunk-bounded`, or `not-applicable` |
| `default_gate` | Whether routine validation executes the demo |
| `required_features` | Comma-separated capability names or `current` |
| `status` | `runnable`, `constrained`, `gated`, or `external` |

`runnable`, `constrained`, and `external` entries must reference an existing
script. `gated` entries may name planned locations, but they must use
`default_gate=no`. A whole-file implementation must never be described as
chunk-bounded merely because its result is later streamed to a client.

Implementation layers describe where the substantive operation occurs:

- `mlpl`: parsing or transformation is expressed in MLPL;
- `mlpl-native`: MLPL owns the algorithm and a generic native boundary supplies
  I/O, transport, or rendering;
- `external`: a named external tool performs the operation as an explicit
  oracle, baseline, compatibility path, or fallback.

Runnable demo recipes are not test transcripts. Internal assertions may gate
execution, but displayed output must narrate the scenario, implementation
boundary, resource budgets, representative result, and interpretation without
ending at a bare PASS or dumping an unexplained internal structure.
