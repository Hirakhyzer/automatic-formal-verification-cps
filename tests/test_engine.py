from cpsverify.engine import VerificationEngine, VerificationRequest


def test_engine_report_fields():
    r = VerificationEngine().verify(VerificationRequest("battery", "interval", steps=5))
    assert r.domain == "battery"
    assert r.method == "interval"
    assert r.status in {"VERIFIED_SAFE", "POTENTIALLY_UNSAFE", "UNKNOWN"}
    assert r.assumptions


def test_both_methods_execute_all_domains():
    engine = VerificationEngine()
    for domain in ("battery", "water", "robot", "railway"):
        for method in ("interval", "zonotope"):
            r = engine.verify(VerificationRequest(domain, method, steps=3))
            assert r.steps == 3
