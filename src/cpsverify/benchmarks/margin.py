from cpsverify.reachability import reach_interval
from cpsverify.properties import check_safety
from cpsverify.status import VerificationStatus


def _status(case):
    fp = reach_interval(case.system, case.initial_set, case.default_steps)
    return check_safety(fp, case.properties[0]).status


def verified_disturbance_margin(case_factory, low=0.0, high=5.0, iterations=24):
    """Bracket and bisect a scalar disturbance multiplier.

    The factory must use ``attack_scale`` monotonically to enlarge the bounded
    disturbance set. If the nominal case is not verified, no positive verified
    margin is claimed. If the supplied high endpoint is still verified, the
    result reports only a lower bound (>= high) and does not invent an unsafe
    endpoint.
    """
    low_status = _status(case_factory(attack_scale=low))
    high_status = _status(case_factory(attack_scale=high))
    if low_status != VerificationStatus.VERIFIED_SAFE:
        return {
            "nominal_status": low_status.value,
            "verified_safe_scale_lower_bound": None,
            "first_not_verified_scale_upper_bound": low,
            "bracketed": False,
        }
    if high_status == VerificationStatus.VERIFIED_SAFE:
        return {
            "nominal_status": low_status.value,
            "verified_safe_scale_lower_bound": high,
            "first_not_verified_scale_upper_bound": None,
            "bracketed": False,
        }
    safe, unsafe = low, high
    for _ in range(iterations):
        mid = (safe + unsafe) / 2.0
        status = _status(case_factory(attack_scale=mid))
        if status == VerificationStatus.VERIFIED_SAFE:
            safe = mid
        else:
            unsafe = mid
    return {
        "nominal_status": low_status.value,
        "verified_safe_scale_lower_bound": safe,
        "first_not_verified_scale_upper_bound": unsafe,
        "bracketed": True,
    }
