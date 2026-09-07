from cpsverify.models import DiscreteLinearSystem, HybridAutomaton, HybridMode, Transition
from cpsverify.sets import Interval
from cpsverify.reachability import reach_hybrid_interval


def test_hybrid_transition_branch_created():
    sys1 = DiscreteLinearSystem([[1.0]], c=[1.0], disturbance_set=Interval([0],[0]), name="m1")
    sys2 = DiscreteLinearSystem([[1.0]], c=[0.0], disturbance_set=Interval([0],[0]), name="m2")
    aut = HybridAutomaton(
        modes={"normal": HybridMode("normal", sys1), "safe": HybridMode("safe", sys2)},
        transitions=[Transition("normal", "safe", Interval([1.5],[100]), name="enter_safe")],
        initial_mode="normal",
    )
    fp = reach_hybrid_interval(aut, Interval([0],[0]), 3)
    assert any(item.mode == "safe" for item in fp.sets)


def test_hybrid_branch_cap_marks_incomplete():
    sys = DiscreteLinearSystem([[1.0]], disturbance_set=Interval([0],[0]))
    aut = HybridAutomaton(
        modes={"a": HybridMode("a", sys), "b": HybridMode("b", sys)},
        transitions=[Transition("a", "b", Interval([-1],[1])), Transition("b", "a", Interval([-1],[1]))],
        initial_mode="a",
    )
    fp = reach_hybrid_interval(aut, Interval([0],[0]), 5, max_branches=1)
    assert not fp.sound_overapproximation
