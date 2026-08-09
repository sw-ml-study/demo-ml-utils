# LEFTS-Inspired Capability Contract

The first LEFTS-inspired experiment runs against the selected `mlpl-repl` and
tests the language mechanisms before proposing an API. Run it with:

```sh
just lefts-capabilities
```

The runner prints the binary version and commit, then demonstrates:

- named callable references passed, returned, and stored in a record;
- partial application as callable data without lexical closure capture;
- `each`, `map_ok`, `table`, `atop`, and `over`;
- deterministic inspection of a computation description;
- a bounded mean-fit callable and prediction callable invoked through that
  description.

## Capability matrix

| Requirement | Exact supported form | Result and classification |
| --- | --- | --- |
| Function as a value | `:u:name` or quoted builtin reference | supported |
| Staged callable | `call(:u:fn, bound...)` returns a partial containing bound data | supported; this is not lexical closure capture |
| Callable registry | record fields hold named references and are invoked with `call` | supported |
| Returned computation | a function returns a record containing `fit`, `predict`, and descriptive data | supported |
| Collection mapping | `each(:u:scalar_fn, numeric_array)` preserves the input shape | supported for scalar-returning element functions |
| Result mapping | `map_ok(:u:fn, result)` maps `ok` and preserves `err` | supported |
| Immediate composition | `atop` and `over`; `table` supplies outer application | supported |
| Inspection | `record_keys` plus ordinary field access and printed callable names | supported and deterministic |
| Arrays of callable records | heterogeneous record/callable cells inside numeric arrays | intentionally unsupported; use numeric context arrays plus a record registry |
| Generic `Functor` protocol | one polymorphic `fmap` over arbitrary containers | absent; `ERGONOMICS_ONLY` until repeated use proves a coherent protocol |
| Lexical closures | anonymous callable capturing its environment | absent, but not required by this contract because named references and partials suffice |

There are no `LANGUAGE_EXPRESSIVENESS_GAP` or `NATIVE_CAPABILITY_GAP`
blockers for the next Split/Lift baseline.

## Functor, endofunctor, and endomorphism

A functor maps both objects and the morphisms between them from one category to
another, preserving identity and composition. An endofunctor is a functor whose
source and target are the same category. An endomorphism is a morphism from one
object to itself.

Consequently, seeing a model transformation with a type-like shape `M -> M`
does not establish a functor. It might describe an endomorphism, but a functor
claim additionally requires a defined mapping of morphisms and evidence for
the identity and composition laws. The demo therefore uses
“endofunctor-like computation transformation” for the LEFTS pattern and avoids
claiming a formal model category.

The executable evidence is deliberately narrower:

- `each(identity, xs) == xs` checks identity for array mapping;
- mapping increment and then double equals mapping their composition;
- `map_ok` changes the success payload and preserves the error branch.

These checks support functor-like descriptions of the two mapping operations.
They do not prove that every LEFTS-inspired model transformation is a functor.

## Smallest current computation contract

The supported representation is an inspectable record containing a name,
kind, description, and named `fit` and `predict` callable references. `fit`
returns a bounded parameter record; `predict` consumes that record. Named
references are late-bound, and partials carry bound data but do not capture a
lexical environment.

This is sufficient for the next explicit Split/Lift experiment. No
`LANGUAGE_EXPRESSIVENESS_GAP`, `NATIVE_CAPABILITY_GAP`, or new generic `fmap`
has been demonstrated. Arrays cannot be used as heterogeneous containers of
callables; records are the intentional computation registry representation.
