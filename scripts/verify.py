#!/usr/bin/env python3
import argparse, json
from cpsverify.engine import VerificationEngine, VerificationRequest
from cpsverify.domains import list_cases

p = argparse.ArgumentParser()
p.add_argument("--domain", choices=list_cases(), default="battery")
p.add_argument("--method", choices=["interval", "zonotope"], default="interval")
p.add_argument("--steps", type=int)
p.add_argument("--attack-scale", type=float, default=1.0)
p.add_argument("--output")
a = p.parse_args()
report = VerificationEngine().verify(VerificationRequest(a.domain, a.method, a.steps, a.attack_scale))
text = json.dumps(report.to_dict(), indent=2)
print(text)
if a.output:
    from pathlib import Path
    Path(a.output).write_text(text + "\n")
