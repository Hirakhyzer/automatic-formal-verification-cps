# Hybrid systems

Cyber-physical systems often have discrete modes with different continuous/discrete dynamics, for example `NORMAL`, `DEGRADED`, and `EMERGENCY`.

The v0.1 hybrid abstraction contains:

- named affine modes;
- axis-aligned mode invariants;
- axis-aligned guards;
- affine reset maps;
- conservative branch retention when a guard is reachable.

This is a research scaffold, not a standards-compliant hybrid-automata verifier. The key scientific requirement is that any branch truncation or unsupported feature results in `UNKNOWN` rather than an unsound safe claim.
