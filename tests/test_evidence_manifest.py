from cpsverify.engine import VerificationEngine, VerificationReport, VerificationRequest
from cpsverify.evidence_manifest import SCHEMA_VERSION, build_evidence_manifest


def test_manifest_records_verification_context_and_assumptions() -> None:
    request = VerificationRequest("battery", "interval", steps=5, attack_scale=1.25)
    report = VerificationEngine().verify(request)

    manifest = build_evidence_manifest(report, request, run_id="test-run")

    assert manifest["schema_version"] == SCHEMA_VERSION
    assert manifest["run_id"] == "test-run"
    assert manifest["domain"] == "battery"
    assert manifest["method"]["name"] == "interval"
    assert manifest["method"]["configuration"]["attack_scale"] == 1.25
    assert manifest["horizon"]["steps"] == 5
    assert manifest["assumptions"]
    assert all(item["status"] == "explicit" for item in manifest["assumptions"])
    assert manifest["result"]["status"] == report.status
    assert manifest["reproducibility"]["verification_request"]["domain"] == "battery"


def test_zonotope_manifest_records_generator_limit() -> None:
    request = VerificationRequest(
        "water",
        "zonotope",
        steps=3,
        max_generators=17,
    )
    report = VerificationEngine().verify(request)

    manifest = build_evidence_manifest(report, request)

    assert manifest["method"]["configuration"]["max_generators"] == 17


def test_unknown_result_is_never_marked_complete() -> None:
    request = VerificationRequest("battery", "interval", steps=2)
    report = VerificationReport(
        domain="battery",
        method="interval",
        status="UNKNOWN",
        property_name="synthetic_property",
        steps=2,
        horizon=2.0,
        first_intersection_step=None,
        first_intersection_time=None,
        reason="synthetic incomplete computation",
        assumptions=["bounded disturbance"],
        overlap=None,
        model_notes="synthetic test report",
    )

    manifest = build_evidence_manifest(report, request)

    assert manifest["result"]["complete"] is False
    assert manifest["result"]["notes"].startswith("Result is conditional")


def test_manifest_contains_reproducibility_metadata() -> None:
    request = VerificationRequest("robot", "interval", steps=2)
    report = VerificationEngine().verify(request)

    manifest = build_evidence_manifest(
        report,
        request,
        configuration_path="configs/robot.yaml",
    )

    reproducibility = manifest["reproducibility"]
    assert reproducibility["python_version"]
    assert reproducibility["platform"]
    assert reproducibility["configuration_path"] == "configs/robot.yaml"
