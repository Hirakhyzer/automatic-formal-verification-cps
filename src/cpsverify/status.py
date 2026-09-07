from enum import Enum


class VerificationStatus(str, Enum):
    VERIFIED_SAFE = "VERIFIED_SAFE"
    POTENTIALLY_UNSAFE = "POTENTIALLY_UNSAFE"
    UNKNOWN = "UNKNOWN"
