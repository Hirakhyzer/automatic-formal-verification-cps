# Reproducibility

Recommended baseline workflow:

```bash
python -m pip install -e ".[dev]"
pytest -q
python scripts/run_demo.py
python scripts/run_benchmarks.py
python scripts/run_margin_sweep.py
```

Record the commit SHA, Python version, NumPy version, OS, and hardware for publication timing results.

Monte-Carlo helpers use explicit seeds. Formal interval/zonotope propagation is deterministic for a fixed model and environment.
