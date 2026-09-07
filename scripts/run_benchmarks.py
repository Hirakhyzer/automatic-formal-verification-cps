#!/usr/bin/env python3
import json, time
from pathlib import Path
from cpsverify.domains import list_cases, get_case
from cpsverify.engine import VerificationEngine, VerificationRequest
from cpsverify.benchmarks import monte_carlo_envelope

engine = VerificationEngine()
rows = []
for domain in list_cases():
    case = get_case(domain)
    for method in ("interval", "zonotope"):
        t0 = time.perf_counter()
        r = engine.verify(VerificationRequest(domain=domain, method=method))
        rows.append({**r.to_dict(), "elapsed_s": time.perf_counter() - t0})
    t0 = time.perf_counter()
    monte_carlo_envelope(case.system, case.initial_set, case.default_steps, samples=1000, seed=7)
    rows.append({"domain": domain, "method": "monte_carlo_1000", "status": "NOT_A_PROOF",
                 "steps": case.default_steps, "horizon": case.default_steps*case.system.dt,
                 "elapsed_s": time.perf_counter() - t0})
Path("results").mkdir(exist_ok=True)
Path("results/v0_1_benchmark.json").write_text(json.dumps(rows, indent=2) + "\n")
print(json.dumps(rows, indent=2))
