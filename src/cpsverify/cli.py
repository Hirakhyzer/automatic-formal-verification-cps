import argparse
import json
from pathlib import Path

from .domains import list_cases
from .engine import VerificationEngine, VerificationRequest
from .evidence_manifest import build_evidence_manifest


def build_parser():
    p = argparse.ArgumentParser(description="Reachability-based CPS safety verifier")
    p.add_argument("domain", choices=list_cases())
    p.add_argument("--method", choices=["interval", "zonotope"], default="interval")
    p.add_argument("--steps", type=int)
    p.add_argument("--attack-scale", type=float, default=1.0)
    p.add_argument("--json", action="store_true")
    p.add_argument(
        "--evidence-manifest",
        help="Write an auditable verification evidence manifest to this JSON path.",
    )
    return p


def main(argv=None):
    args = build_parser().parse_args(argv)
    request = VerificationRequest(
        domain=args.domain,
        method=args.method,
        steps=args.steps,
        attack_scale=args.attack_scale,
    )
    report = VerificationEngine().verify(request)

    if args.json:
        print(json.dumps(report.to_dict(), indent=2))
    else:
        print(f"Domain: {report.domain}")
        print(f"Method: {report.method}")
        print(f"Property: {report.property_name}")
        print(f"Horizon: {report.horizon}")
        print(f"STATUS: {report.status}")
        print(report.reason)

    if args.evidence_manifest:
        manifest = build_evidence_manifest(report, request)
        Path(args.evidence_manifest).write_text(
            json.dumps(manifest, indent=2) + "\n",
            encoding="utf-8",
        )


if __name__ == "__main__":
    main()
