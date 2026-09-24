# Verification Evidence Manifest

## Purpose

Formal-verification results are only meaningful when their assumptions, model boundary, uncertainty bounds, algorithm configuration, and completeness status are preserved with the result.

This repository therefore defines a **verification evidence manifest**: a machine-readable record intended to accompany benchmark or verification outputs.

The manifest is not a certificate. It is an audit artifact that makes the conditions behind a verification claim inspectable and reproducible.

## Why this matters

A result such as `VERIFIED_SAFE` is conditional on the represented model and verification assumptions. Without an explicit record, it is easy to lose the distinction between:

- the physical system and its reduced-order mathematical model;
- represented floating-point coefficients and ideal real-valued parameters;
- bounded uncertainty and unmodeled uncertainty;
- a completed over-approximation and an incomplete computation;
- finite-horizon verification and unrestricted safety;
- a potential unsafe-set intersection and a concrete counterexample.

The evidence manifest makes those boundaries visible.

## Required evidence categories

Each run should record:

1. **Run identity** — unique run identifier, timestamp, and ideally Git commit.
2. **Domain and model** — model name, representation, parameter provenance, and notes.
3. **Property** — property name, unsafe-set definition, and semantics.
4. **Verification method** — interval, zonotope, hybrid, or future method plus its configuration.
5. **Horizon** — the exact finite verification horizon.
6. **Assumptions** — explicit statements with validation status.
7. **Uncertainty bounds** — initial set, input bounds, disturbance bounds, and bounded cyber/fault effects.
8. **Result** — verification status, completeness, unsafe intersection step if any, and candidate witness information.
9. **Reproducibility context** — runtime version, platform, random seed where sampling is involved, and configuration path.

## Assumption status

Assumptions use one of four states:

- `explicit` — stated but not independently validated;
- `validated` — supported by a documented source or experiment;
- `unvalidated` — known to require validation before stronger claims are made;
- `violated` — known not to hold for the run or target context.

A `VERIFIED_SAFE` result with unvalidated assumptions can still be mathematically correct relative to the represented model, but the manifest prevents that result from being mistaken for evidence about a broader physical system.

## Result semantics

The manifest accepts the repository's three verification states:

- `VERIFIED_SAFE`
- `POTENTIALLY_UNSAFE`
- `UNKNOWN`

The `complete` field is required because a nominal status should never hide a computation that lost its sound over-approximation guarantee.

## Schema

The machine-readable definition is stored at:

```text
schemas/verification-evidence.schema.json
```

Future verification and benchmark commands should be able to emit manifests that validate against this schema.

## Example

```json
{
  "run_id": "battery-interval-001",
  "timestamp_utc": "2026-09-24T12:00:00Z",
  "git_commit": "<commit-sha>",
  "domain": "battery",
  "model": {
    "name": "reduced-order battery model",
    "representation": "discrete-time affine",
    "parameter_source": "synthetic research configuration"
  },
  "property": {
    "name": "temperature_below_60C",
    "unsafe_set": "temperature >= 60",
    "semantics": "finite-horizon avoidance"
  },
  "method": {
    "name": "interval",
    "configuration": {
      "outward_rounding": true
    },
    "soundness_boundary": "represented floating-point model"
  },
  "horizon": 40,
  "assumptions": [
    {
      "id": "A1",
      "statement": "all disturbances remain inside the configured disturbance box",
      "status": "explicit",
      "evidence": "benchmark configuration"
    }
  ],
  "uncertainty": {
    "initial_set": "configured interval box",
    "input_bounds": "configured control bounds",
    "disturbance_bounds": "configured disturbance box",
    "cyber_effect_bounds": "configured abstract bounded effect"
  },
  "result": {
    "status": "VERIFIED_SAFE",
    "complete": true,
    "first_intersection_step": null,
    "candidate_witness_region": null,
    "notes": "conditional on recorded assumptions"
  }
}
```

## Research value

This addition strengthens the project in three ways.

First, it separates **proof result** from **evidence provenance**. Second, it creates a reproducible artifact suitable for later benchmark comparison across domains and algorithms. Third, it prepares the repository for assurance-case-style research where each safety claim must be linked to assumptions and evidence rather than reported as a bare status string.

## Planned extensions

- CLI export using `--evidence-manifest <path>`;
- automatic Git commit and environment capture;
- JSON Schema validation in tests and CI;
- manifest bundles for benchmark suites;
- assumption-change diffs between verification runs;
- integration with digital-twin uncertainty updates;
- evidence-to-claim traceability for structured assurance cases.
