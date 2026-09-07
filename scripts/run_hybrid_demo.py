#!/usr/bin/env python3
from cpsverify.models import DiscreteLinearSystem, HybridAutomaton, HybridMode, Transition
from cpsverify.sets import Interval
from cpsverify.reachability import reach_hybrid_interval

normal = DiscreteLinearSystem([[1.0]], c=[0.12], disturbance_set=Interval([-0.01],[0.01]), name="normal")
degraded = DiscreteLinearSystem([[0.96]], c=[0.02], disturbance_set=Interval([-0.02],[0.02]), name="degraded")
automaton = HybridAutomaton(
    modes={
        "NORMAL": HybridMode("NORMAL", normal, Interval([-10],[2.0])),
        "DEGRADED": HybridMode("DEGRADED", degraded, Interval([-10],[3.0])),
    },
    transitions=[Transition("NORMAL", "DEGRADED", Interval([0.8],[10]), name="protective_transition")],
    initial_mode="NORMAL",
)
flowpipe = reach_hybrid_interval(automaton, Interval([0.0],[0.1]), 12)
print(f"sets={len(flowpipe.sets)} sound_overapproximation={flowpipe.sound_overapproximation}")
print("modes_reached=", sorted({x.mode for x in flowpipe.sets}))
