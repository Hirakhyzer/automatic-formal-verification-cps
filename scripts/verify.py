#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

from cpsverify.domains import list_cases
from cpsverify.engine import VerificationEngine, VerificationRequest
from cpsverify.evidence_manifest import build_evidence_manifest


p = argparse.ArgumentParser()
p.add_argument("--domain", choices=list_cases(), default="battery")
p.add_argument("--method", choices=["interval", "zonotope"], default="interval")
p.add_argument("--steps", type=int)
p.add_argument("--attack-scale", type=float, default=1.0)
p.add_argument("--output")
p.add_argument(
    "--evidence-manifest",
    help="Write a verification evidence manifest JSON file for this run.",
)
a = p.parse_args()

request = VerificationRequest(a.domain, a.method, a.steps, a.attack_scale)
report = VerificationEngine().verify(request)
text = json.dumps(report.to_dict(), indent=2)
print(text)

if a.output:
    Path(a.output).write_text(text + "\n", encoding="utf-8")

if a.evidence_manifest:
    manifest = build_evidence_manifest(report, request)
    Path(a.evidence_manifest).write_text(
        json.dumps(manifest, indent=2) + "\n",
        encoding="utf-8",
    )
