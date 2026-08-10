# Progressive Built-In Help Escalation

`just help-escalation` demonstrates the mechanics proposed by the research in
`built-in-help-escalation-demo.txt` without requiring a trained model, browser,
server, or network.

## What it solves

A small browser-resident helper should answer simple, grounded sw-MLPL
questions, but it should not hallucinate missing documentation, diagnose a
program without its runtime context, claim repository access, or silently send
private code to a larger assistant. The demo makes those boundaries executable
before choosing retrieval models, Engram, embeddings, or answer generators.

This recipe is deliberately not trained. The companion
[`just trained-help-engram`](trained-help-engram.md) performs actual CPU Adam
updates on an Engram route classifier and feeds learned class proposals toward
this non-learned authority boundary.

## Contract

Every request carries bounded feature/evidence fields. Initially these are
explicit fixtures; later lexical retrieval, a learned classifier, editor tools,
or an Engram-assisted model may calculate them. `u:help_route` returns:

| Outcome | Meaning | Offered tier |
|---|---|---|
| `Answer` | Current documentation and a runnable example ground the answer | browser |
| `NeedDocs` | No authoritative current-version match | rebuild/refresh browser index |
| `NeedProgramContext` | Source/runtime/shape evidence is required | local `sw-mlpl-serve` |
| `NeedRepository` | Implementation, history, or multiple files are required | local `sw-mlpl-serve` |
| `NeedReasoning` | Evidence exists but the bounded specialist cannot compose the answer safely | user-selected external/local large model |
| `OutsideDomain` | Not an sw-MLPL question | none |

Priority is safety-oriented: outside-domain rejection, repository need,
reasoning need, missing program context, stale/missing docs, then grounded
answer. A retrieval match alone is insufficient.

## Escalation bundle

Every result contains a uniform inert bundle with the question, language
version, reason, retrieved-document label, optional runtime error, and optional
source/transcript. Source and transcript are replaced with `[withheld]` unless
their individual consent flag is set. The record always states:

```text
automatic_send = 0
automatic_execute = 0
```

The Web UI could render this as a review screen or “Copy for AI” artifact.
`sw-mlpl-serve` could later accept the same schema and enrich it with AST,
shape, repository, and test evidence. No provider-specific API belongs in this
pure routing layer.

## Demonstrated scenarios

1. `drop` usage is answered locally with citation and runnable example.
2. A rank mismatch requests program context and includes explicitly consented
   source plus the runtime observation.
3. A parser implementation question routes to repository-capable local help.
4. A category-theory comparison offers a portable stronger-model bundle while
   withholding unconsented private source and transcript.
5. A stale-version documentation hit requests a current index rather than
   answering from memory.
6. A restaurant request is declined as outside the specialist's domain.

The test also proves schema and question-size rejection. Later acceptance
should add bundle byte/source/transcript exhaustion, malformed consent flags,
retrieval-score calibration, adversarial prompt injection, and deterministic
serialization.

## Later sw-MLPL integration

The downstream experiment supports, but does not yet justify, these upstream
pieces:

- a versioned `HelpRequest`/`HelpResult` protocol shared by Web and serve;
- read-only interpreter tools for symbol, error, AST, shape, docs, and example
  lookup;
- a local `/help/capabilities` and help-query endpoint;
- UI review/consent controls and portable bundle export;
- optional lexical/semantic retrieval and tiny CPU/WASM inference.

No new language keyword, builtin, Engram primitive, network provider, or core
model API should be added until downstream measurements show a general gap.
Engram remains an experimental Tier-0 optimization, distinct from the
versioned documentation truth source.
