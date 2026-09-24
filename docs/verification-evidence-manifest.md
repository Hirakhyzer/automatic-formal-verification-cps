# Verification Evidence Manifest

## Purpose

Formal-verification results are only meaningful when their assumptions, model boundary, uncertainty bounds, algorithm configuration, and completeness status are preserved with the result.

This repository therefore implements a **verification evidence manifest**: a machine-readable record that can accompany every verification run.

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

## Implemented workflow

Both verification entry points can now emit an evidence manifest.

Installed CLI:

```bash
cpsverify battery --method interval --evidence-manifest artifacts/battery-evidence.json
```

Repository script:

```bash
python scripts/verify.py \
  --domain battery \
  --method interval \
  --evidence-manifest artifacts/battery-evidence.json
```

The implementation lives in:

```text
src/cpsverify/evidence_manifest.py
```

The machine-readable schema lives in:

```text
schemas/verification-evidence.schema.json
```

## Required evidence categories

Each emitted manifest records:

1. **Schema version** — version of the evidence contract.
2. **Run identity** — run identifier, UTC timestamp, and Git commit when available.
3. **Domain and model** — model identity, representation boundary, parameter provenance, and notes.
4. **Property** — property name, unsafe-set semantics, and finite-horizon interpretation.
5. **Verification method** — interval or zonotope method plus configuration.
6. **Horizon** — exact step count and corresponding modeled time.
7. **Assumptions** — explicit statements with validation status.
8. **Uncertainty bounds** — initial set, input bounds, disturbance bounds, and abstract cyber/fault effects.
9. **Result** — status, completeness, first unsafe intersection metadata, witness-region information, and reason.
10. **Reproducibility context** — Python version, platform, configuration path, and serialized verification request.

## Assumption status

Assumptions use one of four states:

- `explicit` — stated but not independently validated;
- `validated` — supported by a documented source or experiment;
- `unvalidated` — known to require validation before stronger claims are made;
- `violated` — known not to hold for the run or target context.

The current exporter records engine-provided assumptions as `explicit`. Future experiments can promote individual assumptions to `validated` only when supporting evidence is available.

A `VERIFIED_SAFE` result with unvalidated assumptions can still be mathematically correct relative to the represented model, but the manifest prevents that result from being mistaken for evidence about a broader physical system.

## Result semantics

The manifest accepts the repository's three verification states:

- `VERIFIED_SAFE`
- `POTENTIALLY_UNSAFE`
- `UNKNOWN`

An `UNKNOWN` result is always exported with `complete: false`. This prevents an incomplete verification run from being presented as a completed proof artifact.

## Example structure

```json
{
  "schema_version": "1.0.0",
  "run_id": "battery-interval-temperature_below_60C-40",
  "timestamp_utc": "2026-09-24T12:00:00Z",
  "git_commit": "<commit-sha-or-null>",
  "domain": "battery",
  "method": {
    "name": "interval",
    "configuration": {
      "steps": 40,
      "attack_scale": 1.0,
      "property_index": 0
    },
    "soundness_boundary": "represented floating-point model and configured uncertainty bounds"
  },
  "horizon": {
    "steps": 40,
    "time": 40.0
  },
  "assumptions": [
    {
      "id": "A1",
      "statement": "all disturbances remain inside the configured disturbance box",
      "status": "explicit",
      "evidence": "verification flowpipe assumptions"
    }
  ],
  "result": {
    "status": "VERIFIED_SAFE",
    "complete": true,
    "first_intersection_step": null,
    "first_intersection_time": null,
    "candidate_witness_region": null,
    "reason": "...",
    "notes": "Result is conditional on the recorded model and assumptions."
  }
}
```

## Research value

This capability strengthens the project in three ways.

First, it separates **proof result** from **evidence provenance**. Second, it creates a reproducible artifact suitable for benchmark comparison across domains and algorithms. Third, it supports assurance-case-style research where each safety claim must be linked to assumptions and evidence rather than reported as a bare status string.

## Current safeguards

The implementation deliberately:

- keeps the evidence manifest separate from the core `VerificationReport`;
- records the full `VerificationRequest` used to produce the result;
- captures the Git commit when the repository context is available;
- captures Python and platform information;
- records zonotope generator limits when that method is selected;
- preserves overlap/witness-region information when available;
- marks `UNKNOWN` computations incomplete;
- describes cyber effects only as bounded abstract uncertainty.

## Planned extensions

- JSON Schema validation as a CI gate;
- manifest bundles for benchmark suites;
- cryptographic hashing of model/configuration inputs;
- assumption-change diffs between verification runs;
- integration with digital-twin uncertainty updates;
- evidence-to-claim traceability for structured assurance cases;
- experiment IDs that link manifests directly to published benchmark tables.
