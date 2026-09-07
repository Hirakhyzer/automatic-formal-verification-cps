import argparse, json
from .engine import VerificationEngine, VerificationRequest
from .domains import list_cases


def build_parser():
    p = argparse.ArgumentParser(description="Reachability-based CPS safety verifier")
    p.add_argument("domain", choices=list_cases())
    p.add_argument("--method", choices=["interval", "zonotope"], default="interval")
    p.add_argument("--steps", type=int)
    p.add_argument("--attack-scale", type=float, default=1.0)
    p.add_argument("--json", action="store_true")
    return p


def main(argv=None):
    args = build_parser().parse_args(argv)
    report = VerificationEngine().verify(VerificationRequest(
        domain=args.domain, method=args.method, steps=args.steps, attack_scale=args.attack_scale
    ))
    if args.json:
        print(json.dumps(report.to_dict(), indent=2))
    else:
        print(f"Domain: {report.domain}")
        print(f"Method: {report.method}")
        print(f"Property: {report.property_name}")
        print(f"Horizon: {report.horizon}")
        print(f"STATUS: {report.status}")
        print(report.reason)


if __name__ == "__main__":
    main()
