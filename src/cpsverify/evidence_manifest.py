from __future__ import annotations

from dataclasses import asdict
from datetime import datetime, timezone
import platform
import subprocess
import sys
from typing import Any

from .engine import VerificationReport, VerificationRequest


SCHEMA_VERSION = "1.0.0"


def _git_commit() -> str | None:
    """Return the current Git commit when available without making it mandatory."""
    try:
        completed = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
            timeout=2,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    commit = completed.stdout.strip()
    return commit or None


def build_evidence_manifest(
    report: VerificationReport,
    request: VerificationRequest,
    *,
    run_id: str | None = None,
    configuration_path: str | None = None,
) -> dict[str, Any]:
    """Build an auditable manifest for one formal-verification run.

    The manifest records the verification result together with the assumptions
    and runtime context required to interpret it. It is intentionally separate
    from ``VerificationReport`` so that proof results remain distinct from
    provenance and assurance evidence.
    """
    timestamp = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    effective_run_id = run_id or (
        f"{report.domain}-{report.method}-{report.property_name}-{report.steps}"
    )

    assumption_entries = [
        {
            "id": f"A{index}",
            "statement": statement,
            "status": "explicit",
            "evidence": "verification flowpipe assumptions",
        }
        for index, statement in enumerate(report.assumptions, start=1)
    ]

    method_configuration: dict[str, Any] = {
        "steps": report.steps,
        "attack_scale": request.attack_scale,
        "property_index": request.property_index,
    }
    if request.method == "zonotope":
        method_configuration["max_generators"] = request.max_generators

    complete = report.status != "UNKNOWN"

    return {
        "schema_version": SCHEMA_VERSION,
        "run_id": effective_run_id,
        "timestamp_utc": timestamp,
        "git_commit": _git_commit(),
        "domain": report.domain,
        "model": {
            "name": report.domain,
            "representation": "repository-defined reduced-order CPS model",
            "parameter_source": "versioned repository configuration",
            "notes": report.model_notes,
        },
        "property": {
            "name": report.property_name,
            "unsafe_set": "defined by the selected repository property",
            "semantics": "finite-horizon unsafe-set avoidance",
        },
        "method": {
            "name": report.method,
            "configuration": method_configuration,
            "soundness_boundary": (
                "represented floating-point model and configured uncertainty bounds"
            ),
        },
        "horizon": {
            "steps": report.steps,
            "time": report.horizon,
        },
        "assumptions": assumption_entries,
        "uncertainty": {
            "initial_set": "domain-defined bounded initial set",
            "input_bounds": "domain-defined bounded inputs",
            "disturbance_bounds": "domain-defined bounded disturbances",
            "cyber_effect_bounds": (
                f"domain-defined abstract bounded effect scaled by {request.attack_scale}"
            ),
        },
        "result": {
            "status": report.status,
            "complete": complete,
            "first_intersection_step": report.first_intersection_step,
            "first_intersection_time": report.first_intersection_time,
            "candidate_witness_region": report.overlap,
            "reason": report.reason,
            "notes": "Result is conditional on the recorded model and assumptions.",
        },
        "reproducibility": {
            "python_version": sys.version.split()[0],
            "platform": platform.platform(),
            "configuration_path": configuration_path,
            "verification_request": asdict(request),
        },
    }
