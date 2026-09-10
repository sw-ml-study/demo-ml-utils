# Mathematical notation rules

Every equation this repository displays must be **complete**. A reader must be
able to reconstruct the computation from what is shown, without consulting the
source paper and without inferring anything the notation left out.

These rules bind demo output, `@formula` annotations, documentation, and any
rendered SVG.

## 1. Summations carry explicit limits

A bare `∑_q` is not acceptable. Both bounds are always shown.

Stacked form, used wherever vertical space allows — demo output, documentation:

```text
               Q      M_w    N_w
  y[r,x,y]  =  ∑      ∑      ∑     W[r,q,u,v] · X[q, x+u, y+v]
              q=1    u=1    v=1
```

Inline form, used in `@formula` annotations, one-line summaries, and SVG:

```text
y[r,x,y] = ∑(q=1..Q) ∑(u=1..M_w) ∑(v=1..N_w) W[r,q,u,v] · X[q, x+u, y+v]
```

Both are complete. `∑_q ∑_u ∑_v W · X` is not, and must not appear.

## 2. Every symbol is defined

An equation is displayed with a symbol table naming each index, its range, and
what it selects. No symbol appears in an equation without a definition
adjacent to it.

| Symbol | Range | Meaning |
|---|---|---|
| `r` | output filters | selects the output feature map |
| `q` | input channels | selects the input feature map |
| `u`, `v` | kernel rows, columns | position inside the kernel window |
| `x`, `y` | output positions | position in the output feature map |
| `Q` | — | number of input channels |
| `M_w`, `N_w` | — | kernel height and width |

## 3. Index base is stated, and the translation is shown

Published equations are usually 1-based. MLPL arrays are 0-based. The demo must
show both and the mapping between them, because silently reindexing is exactly
the kind of shortcut that makes an equation and its implementation disagree
without either looking wrong.

Where a source uses `q = 1..Q`, the implementation's loop runs `0..Q-1` and the
demo says so in the same breath as the equation.

## 4. Convolution versus cross-correlation is named

The equation above uses `X[q, x+u, y+v]`, not `X[q, x-u, y-v]`. That is
**cross-correlation**: the kernel is not flipped. Every mainstream CNN
framework does this and calls it convolution, and the native `conv2d` builtin
matches it, but the demo names the discrepancy rather than inheriting it
silently. A demo that claims to implement a mathematical convolution while
computing a correlation is not honest about its own arithmetic.

## 5. Rendering targets

| Target | Form | Mechanism |
|---|---|---|
| Terminal demo output | stacked, Unicode | `print` |
| `@formula` annotation | inline | preserved as data, readable via `annotations()` |
| Documentation | LaTeX with `\sum_{q=1}^{Q}` | GitHub renders `$$...$$` natively |
| SVG / web | inline | `svg(text, "equation")`, no LaTeX toolchain or network |

`svg(text, "equation")` is upstream's renderer and is used rather than a second
implementation. The `@formula` annotation is the single source of truth for
each equation; other forms are derived from it and must not drift.

## 6. Attribution names what is used and what is not

Citing a paper for one definition does not license implying its contribution is
implemented. Where this repository implements only a source's definitional
equation, the attribution says which section is used and which results are not
implemented.

## The convolution equation, verified against the source

Verified by reading the paper directly (`work/algorithms-11-00159.pdf`, local
and untracked; MDPI returns HTTP 403 to automated fetches).

Zhao, Y.; Wang, D.; Wang, L.; Liu, P. "A Faster Algorithm for Reducing the
Computational Complexity of Convolutional Neural Networks". *Algorithms* 2018,
**11**(10), 159. DOI `10.3390/a11100159`. CC BY 4.0. Received 10 September 2018,
accepted 16 October 2018, published 18 October 2018.

Section 2.1, Equation (1), transcribed exactly:

$$ y_{r,x,y} = \sum_{q=1}^{Q} \sum_{u=1}^{M_w} \sum_{v=1}^{N_w}
   w_{r,q,u,v}\, x_{q,x+u,y+v} $$

Complete symbol table, from the sentence preceding the equation and the one
following it:

| Symbol | Meaning |
|---|---|
| `Q` | number of input feature maps, each of size `Mx × Nx` |
| `R` | number of output feature maps, each of size `My × Ny` |
| `Mw`, `Nw` | convolutional kernel height and width |
| `X`, `Y`, `W` | the input feature map, output feature map, and kernel |
| `x`, `y` | position of the pixel in the feature map |
| `u`, `v` | position of the parameter in the kernel |
| `q` | indexes the input feature map |
| `r` | indexes the output feature map |

Four things this settles that were previously assumed:

1. **Section and equation number are correct.** Section 2.1, Equation (1).
2. **The limits are 1-based**, exactly `q = 1..Q`, `u = 1..M_w`, `v = 1..N_w`,
   so the 0-based translation rule above is required, not decorative.
3. **The paper writes `x_{q,x+u,y+v}`, not `x_{q,x-u,y-v}`.** The kernel is not
   flipped. Equation (1) therefore defines cross-correlation, which is what
   every mainstream framework calls convolution and what `conv2d` computes.
   Rule 4 applies to this equation specifically, not hypothetically.
4. **Equation (1) contains no bias and no activation.** A demo rung that adds
   `+ b` and `relu` is going beyond what this equation states and must say so
   rather than implying the paper defines a layer that way.

Two fidelity notes for anything that reproduces the equation:

- The paper uses **lowercase** `y`, `w`, `x` for the indexed elements and
  reserves uppercase `X`, `Y`, `W` for the feature maps and kernel as whole
  objects. Bracket-index transliterations such as `W[r,q,u,v]` are acceptable
  for terminal rendering, but should not silently promote the elements to
  uppercase in a context claiming to quote the paper.
- The paper itself then rewrites Equation (1) as Equation (2),
  `y_r = \sum_{q=1}^{Q} w_{r,q} * x_q`, collapsing the two kernel sums into a
  convolution operator. The demo's move from three nested reductions to one is
  the same move the source makes, one step further.

### Attribution

The paper is CC BY 4.0, so the equation may be reproduced with attribution.
This repository implements **only Equation (1)**, the definition. The paper's
contribution — a faster algorithm combining Winograd minimal filtering with
the Strassen algorithm, reported to save 75% of runtime on VGG — is **not**
implemented here, and no demo may imply otherwise.
