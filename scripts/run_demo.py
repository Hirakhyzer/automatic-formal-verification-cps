#!/usr/bin/env python3
from cpsverify.engine import VerificationEngine, VerificationRequest

engine = VerificationEngine()
for domain in ("battery", "water", "robot", "railway"):
    report = engine.verify(VerificationRequest(domain=domain, method="interval"))
    print(f"{domain:8s} {report.status:20s} {report.property_name}")
