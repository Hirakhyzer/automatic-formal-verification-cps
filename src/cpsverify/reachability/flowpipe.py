from dataclasses import dataclass, field
from typing import Any


@dataclass
class ReachSet:
    step: int
    time: float
    set: Any
    mode: str | None = None


@dataclass
class Flowpipe:
    method: str
    sets: list[ReachSet] = field(default_factory=list)
    sound_overapproximation: bool = True
    assumptions: list[str] = field(default_factory=list)

    def append(self, item: ReachSet):
        self.sets.append(item)

    def __len__(self):
        return len(self.sets)
