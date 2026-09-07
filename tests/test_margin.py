from cpsverify.benchmarks import verified_disturbance_margin
from cpsverify.domains.battery import battery_case
from cpsverify.domains.robot import robot_case


def test_margin_does_not_invent_unsafe_endpoint():
    r = verified_disturbance_margin(battery_case, high=0.1, iterations=4)
    assert r["verified_safe_scale_lower_bound"] == 0.1
    assert r["first_not_verified_scale_upper_bound"] is None


def test_robot_nominal_case_is_verified_for_margin_experiment():
    r = verified_disturbance_margin(robot_case, high=8.0, iterations=8)
    assert r["nominal_status"] == "VERIFIED_SAFE"
