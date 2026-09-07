#!/usr/bin/env python3
import json
from cpsverify.domains.battery import battery_case
from cpsverify.domains.water import water_case
from cpsverify.domains.robot import robot_case
from cpsverify.domains.railway import railway_case
from cpsverify.benchmarks import verified_disturbance_margin

factories = {"battery": battery_case, "water": water_case, "robot": robot_case, "railway": railway_case}
out = {name: verified_disturbance_margin(factory, high=8.0) for name, factory in factories.items()}
print(json.dumps(out, indent=2))
