from dataclasses import dataclass
from cpsverify.models import HybridAutomaton
from cpsverify.sets import Interval
from .flowpipe import Flowpipe, ReachSet


@dataclass
class Branch:
    mode: str
    state: Interval


def _clip_invariant(state, invariant):
    if invariant is None:
        return state
    return state.intersection(invariant)


def reach_hybrid_interval(automaton: HybridAutomaton, initial: Interval, steps: int,
                          max_branches: int = 64) -> Flowpipe:
    automaton.validate()
    branches = [Branch(automaton.initial_mode, initial)]
    fp = Flowpipe(
        method="branching interval hybrid reachability",
        sound_overapproximation=True,
        assumptions=[
            "guards/invariants are axis-aligned boxes",
            "transition branching retains both staying and enabled-transition possibilities",
            "branch cap must not be exceeded for a complete result",
        ],
    )
    fp.append(ReachSet(0, 0.0, initial, automaton.initial_mode))
    for k in range(steps):
        new = []
        for b in branches:
            mode = automaton.modes[b.mode]
            propagated = mode.system.step_interval(b.state)
            propagated = _clip_invariant(propagated, mode.invariant)
            if propagated is None:
                continue
            new.append(Branch(b.mode, propagated))
            fp.append(ReachSet(k + 1, (k + 1) * mode.system.dt, propagated, b.mode))
            for tr in automaton.outgoing(b.mode):
                if propagated.intersects(tr.guard):
                    target_state = tr.apply(propagated)
                    target_inv = automaton.modes[tr.target].invariant
                    target_state = _clip_invariant(target_state, target_inv)
                    if target_state is not None:
                        new.append(Branch(tr.target, target_state))
                        fp.append(ReachSet(k + 1, (k + 1) * mode.system.dt, target_state, tr.target))
        if len(new) > max_branches:
            fp.sound_overapproximation = False
            fp.assumptions.append("branch cap exceeded; result marked incomplete")
            new = new[:max_branches]
        branches = new
        if not branches:
            break
    return fp
