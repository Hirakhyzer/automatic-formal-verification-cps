# Architecture

```text
CPS domain model
      │
      ├── initial set X0
      ├── input set U
      ├── disturbance / cyber-effect set W
      └── unsafe property
      │
      ▼
Reachability engine
      ├── outward-rounded intervals
      ├── zonotopes
      └── branching hybrid intervals
      │
      ▼
Flowpipe R0, R1, ... RN
      │
      ▼
Safety checker
      ├── VERIFIED_SAFE
      ├── POTENTIALLY_UNSAFE
      └── UNKNOWN
      │
      ├── overlap / candidate witness region
      └── reproducible verification report
```

The cyber layer never connects to real infrastructure. Bounded cyber effects are mathematical uncertainty sets injected into the model.
