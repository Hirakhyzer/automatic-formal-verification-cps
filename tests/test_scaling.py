from cpsverify.benchmarks import scaling_sweep, synthetic_stable_system


def test_synthetic_scaling_model_and_sweep():
    s = synthetic_stable_system(4)
    assert s.state_dim == 4
    rows = scaling_sweep(dimensions=(2, 4), steps=3)
    assert len(rows) == 4
    assert {r["method"] for r in rows} == {"interval", "zonotope"}
