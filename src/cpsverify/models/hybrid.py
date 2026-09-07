from __future__ import annotations
from dataclasses import dataclass, field
import numpy as np
from cpsverify.sets import Interval
from .linear import DiscreteLinearSystem


@dataclass
class HybridMode:
    name: str
    system: DiscreteLinearSystem
    invariant: Interval | None = None


@dataclass
class Transition:
    source: str
    target: str
    guard: Interval
    reset_matrix: np.ndarray | None = None
    reset_bias: np.ndarray | None = None
    name: str = "transition"

    def apply(self, state: Interval) -> Interval:
        intersected = state.intersection(self.guard)
        if intersected is None:
            raise ValueError("transition guard not intersected")
        if self.reset_matrix is None:
            return intersected
        return intersected.affine_map(self.reset_matrix, self.reset_bias)


@dataclass
class HybridAutomaton:
    modes: dict[str, HybridMode] = field(default_factory=dict)
    transitions: list[Transition] = field(default_factory=list)
    initial_mode: str = ""

    def outgoing(self, mode: str) -> list[Transition]:
        return [t for t in self.transitions if t.source == mode]

    def validate(self):
        if self.initial_mode not in self.modes:
            raise ValueError("initial mode missing")
        for t in self.transitions:
            if t.source not in self.modes or t.target not in self.modes:
                raise ValueError("transition references unknown mode")
