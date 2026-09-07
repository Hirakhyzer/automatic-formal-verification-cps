# Set representations

## Intervals / boxes

A box is

\[
X=[\underline{x},\overline{x}].
\]

It is cheap and easy to audit but loses correlations between state variables, often causing wrapping/conservatism.

## Zonotopes

A zonotope is

\[
Z=c+G[-1,1]^p.
\]

Affine maps preserve correlations encoded by the generator matrix and can be substantially tighter than boxes. The implementation limits generator growth with a conservative box reduction.

## Future representations

Planned research includes constrained zonotopes, support functions, polytopes, star sets, and Taylor-model/interval techniques for nonlinear dynamics.
