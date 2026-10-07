# Unsafe-Intersection Diagnostics

## Motivation

A reachability result marked `POTENTIALLY_UNSAFE` does not necessarily contain a concrete unsafe trajectory. The reachable set is an over-approximation, so its intersection with an unsafe region can be caused either by a genuinely reachable unsafe state or by conservatism in the set representation.

The repository therefore distinguishes **intersection diagnostics** from **counterexample traces**.

## Diagnostic output

For the first reachable-set/unsafe-set intersection, the verification engine now records:

- overlap width in each state dimension;
- overlap volume;
- reachable-set volume;
- unsafe-set volume;
- fraction of the reachable box occupied by the overlap;
- fraction of the unsafe box occupied by the overlap;
- geometric center of the overlap;
- whether the intersection is degenerate in at least one dimension.

The geometric center is named a `candidate_center`. It is useful for follow-up simulation, falsification, or refinement, but it is **not** labeled a concrete counterexample.

## Interpretation

A large overlap fraction can prioritize a verification result for investigation, while a very small overlap may suggest that representation conservatism or boundary contact deserves closer analysis. Neither case proves the existence or absence of a concrete violating execution.

Recommended follow-up workflow:

```text
POTENTIALLY_UNSAFE
       |
       v
intersection diagnostic
       |
       +--> candidate center / overlap geometry
       |
       +--> targeted simulation or optimization
       |
       +--> tighter reachability representation
       |
       +--> assumption / uncertainty sensitivity
       v
concrete witness found OR conservatism reduced OR remains unresolved
```

## Evidence identity

Evidence manifests now separate two identities:

1. `run_id` is unique for an execution by default, preventing repeated equivalent runs from silently sharing an identifier.
2. `evidence_fingerprint_sha256` is deterministic for the verification request and key result semantics, allowing equivalent runs to be grouped and compared reproducibly.

This distinction supports repeated experiments: executions remain individually auditable while equivalent verification outcomes can still be recognized.

## Scientific boundary

The diagnostic layer does not perform trajectory reconstruction, nonlinear falsification, SMT witness extraction, or proof refinement. Those are separate research problems. The current implementation quantifies the geometry already established by the sound reachable-set computation and preserves that information in machine-readable assurance evidence.
