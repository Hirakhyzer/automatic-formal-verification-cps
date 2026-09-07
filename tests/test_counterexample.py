from cpsverify.models import DiscreteLinearSystem
from cpsverify.sets import Interval
from cpsverify.counterexample import sample_counterexample_candidate


def test_sampling_can_find_trivial_counterexample():
    sys = DiscreteLinearSystem([[1.0]], c=[1.0], disturbance_set=Interval([0],[0]))
    found = sample_counterexample_candidate(sys, Interval([0],[0]), Interval([2],[2]), steps=3, samples=1, seed=0)
    assert found is not None and found["step"] == 2
