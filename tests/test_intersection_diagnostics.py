import pytest

from cpsverify.diagnostics import diagnose_intersection
from cpsverify.engine import VerificationReport, VerificationRequest
from cpsverify.evidence_manifest import build_evidence_manifest
from cpsverify.sets import Interval


def test_intersection_diagnostic_quantifies_overlap_without_claiming_trace():
    reachable = Interval([0.0, 0.0], [4.0, 2.0])
    unsafe = Interval([3.0, 1.0], [5.0, 3.0])

    diagnostic = diagnose_intersection(reachable, unsafe)

    assert diagnostic is not None
    assert diagnostic.overlap_widths == pytest.approx((1.0, 1.0))
    assert diagnostic.overlap_volume == pytest.approx(1.0)
    assert diagnostic.reachable_overlap_fraction == pytest.approx(1.0 / 8.0)
    assert diagnostic.unsafe_overlap_fraction == pytest.approx(1.0 / 4.0)
    assert diagnostic.candidate_center == pytest.approx((3.5, 1.5))


def test_disjoint_sets_have_no_intersection_diagnostic():
    reachable = Interval([0.0], [1.0])
    unsafe = Interval([2.0], [3.0])
    assert diagnose_intersection(reachable, unsafe) is None


def _report() -> VerificationReport:
    return VerificationReport(
        domain="battery",
        method="interval",
        status="POTENTIALLY_UNSAFE",
        property_name="temperature-limit",
        steps=10,
        horizon=1.0,
        first_intersection_step=7,
        first_intersection_time=0.7,
        reason="reachable over-approximation intersects unsafe set",
        assumptions=["bounded disturbance"],
        overlap={"lower": [59.0], "upper": [61.0]},
        model_notes="test model",
        intersection_diagnostic={"overlap_volume": 2.0},
    )


def test_default_run_ids_are_unique_but_fingerprint_is_stable():
    request = VerificationRequest(domain="battery", steps=10)
    first = build_evidence_manifest(_report(), request)
    second = build_evidence_manifest(_report(), request)

    assert first["run_id"] != second["run_id"]
    assert first["evidence_fingerprint_sha256"] == second["evidence_fingerprint_sha256"]
    assert len(first["evidence_fingerprint_sha256"]) == 64


def test_intersection_diagnostic_is_preserved_in_evidence_manifest():
    manifest = build_evidence_manifest(_report(), VerificationRequest(domain="battery", steps=10))
    assert manifest["result"]["intersection_diagnostic"] == {"overlap_volume": 2.0}
