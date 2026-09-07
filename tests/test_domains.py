from cpsverify.domains import list_cases, get_case


def test_all_domain_cases_construct():
    assert list_cases() == ["battery", "railway", "robot", "water"]
    for name in list_cases():
        case = get_case(name)
        assert case.system.state_dim == case.initial_set.dim
        assert case.default_steps > 0
        assert case.properties
