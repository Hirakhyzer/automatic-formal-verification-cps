#!/usr/bin/env python3
import json
from pathlib import Path
from cpsverify.benchmarks import scaling_sweep

rows = scaling_sweep()
Path("results").mkdir(exist_ok=True)
Path("results/v0_1_scaling.json").write_text(json.dumps(rows, indent=2) + "\n")
print(json.dumps(rows, indent=2))
