from cpsverify.domains import get_case
from cpsverify.benchmarks import monte_carlo_envelope


def test_monte_carlo_envelope_shape():
    case = get_case("battery")
    lo, hi = monte_carlo_envelope(case.system, case.initial_set, 4, samples=10, seed=1)
    assert lo.shape == hi.shape == (5, 2)
    assert (lo <= hi).all()
