from cpsverify.models import DiscreteLinearSystem
from cpsverify.sets import Interval
from cpsverify.reachability import reach_interval
from cpsverify.properties import SafetyProperty, check_safety
from cpsverify.status import VerificationStatus


def test_verified_safe_when_disjoint():
    sys = DiscreteLinearSystem([[1.0]], disturbance_set=Interval([0],[0]))
    fp = reach_interval(sys, Interval([0],[1]), 3)
    r = check_safety(fp, SafetyProperty("far", Interval([10],[20])))
    assert r.status == VerificationStatus.VERIFIED_SAFE


def test_potentially_unsafe_when_intersecting():
    sys = DiscreteLinearSystem([[1.0]], c=[1.0], disturbance_set=Interval([0],[0]))
    fp = reach_interval(sys, Interval([0],[0]), 3)
    r = check_safety(fp, SafetyProperty("hit", Interval([2.5],[3.5])))
    assert r.status == VerificationStatus.POTENTIALLY_UNSAFE
    assert r.first_intersection_step == 3
    assert r.overlap is not None
