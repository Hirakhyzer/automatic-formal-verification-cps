"""Automatic reachability-based verification for reduced-order CPS models."""

from .diagnostics import IntersectionDiagnostic, diagnose_intersection
from .engine import VerificationEngine, VerificationRequest, VerificationReport
from .status import VerificationStatus

__all__ = [
    "IntersectionDiagnostic",
    "VerificationEngine",
    "VerificationRequest",
    "VerificationReport",
    "VerificationStatus",
    "diagnose_intersection",
]
__version__ = "0.2.0"
