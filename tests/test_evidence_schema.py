import copy
import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator, ValidationError

from cpsverify.engine import VerificationEngine, VerificationRequest
from cpsverify.evidence_manifest import build_evidence_manifest


SCHEMA_PATH = Path(__file__).parents[1] / "schemas" / "verification-evidence.schema.json"


def _validator() -> Draft202012Validator:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema)


@pytest.mark.parametrize("domain,method", [("battery", "interval"), ("water", "zonotope")])
def test_generated_manifest_conforms_to_evidence_schema(domain: str, method: str) -> None:
    request = VerificationRequest(domain, method, steps=3)
    report = VerificationEngine().verify(request)
    manifest = build_evidence_manifest(report, request, run_id="schema-test")

    _validator().validate(manifest)


def test_schema_rejects_malformed_nested_method_configuration() -> None:
    request = VerificationRequest("battery", "interval", steps=2)
    manifest = build_evidence_manifest(VerificationEngine().verify(request), request)
    malformed = copy.deepcopy(manifest)
    malformed["method"]["configuration"]["steps"] = "two"

    with pytest.raises(ValidationError):
        _validator().validate(malformed)


def test_schema_rejects_partial_intersection_diagnostic() -> None:
    request = VerificationRequest("battery", "interval", steps=2)
    manifest = build_evidence_manifest(VerificationEngine().verify(request), request)
    malformed = copy.deepcopy(manifest)
    malformed["result"]["intersection_diagnostic"] = {"overlap_volume": 1.0}

    with pytest.raises(ValidationError):
        _validator().validate(malformed)


def test_schema_rejects_unknown_top_level_fields() -> None:
    request = VerificationRequest("robot", "interval", steps=2)
    manifest = build_evidence_manifest(VerificationEngine().verify(request), request)
    manifest["untracked_provenance"] = "silent schema drift"

    with pytest.raises(ValidationError):
        _validator().validate(manifest)
