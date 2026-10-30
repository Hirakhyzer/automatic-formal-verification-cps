import math

import pytest

from cpsverify.engine import VerificationEngine, VerificationRequest


@pytest.mark.parametrize(
    "verification_request,message",
    [
        (VerificationRequest("battery", "invalid"), "method"),
        (VerificationRequest("battery", steps=0), "steps"),
        (VerificationRequest("battery", attack_scale=-0.01), "attack_scale"),
        (VerificationRequest("battery", property_index=-1), "property_index"),
        (VerificationRequest("battery", "zonotope", max_generators=0), "max_generators"),
    ],
)
def test_invalid_request_shape_fails_before_reachability(verification_request, message) -> None:
    with pytest.raises(ValueError, match=message):
        VerificationEngine().verify(verification_request)


def test_out_of_range_property_index_has_domain_specific_error() -> None:
    verification_request = VerificationRequest("battery", property_index=999)

    with pytest.raises(ValueError, match="property_index.*battery"):
        VerificationEngine().verify(verification_request)


@pytest.mark.parametrize("steps", [True, -1, 1.5, "10"])
def test_steps_requires_positive_integer(steps) -> None:
    with pytest.raises(ValueError, match="steps must be a positive integer"):
        VerificationEngine().verify(VerificationRequest("battery", steps=steps))


@pytest.mark.parametrize("attack_scale", [math.nan, math.inf, -math.inf, True, "1.0"])
def test_attack_scale_requires_finite_number(attack_scale) -> None:
    with pytest.raises(ValueError, match="attack_scale must be a finite number"):
        VerificationEngine().verify(VerificationRequest("battery", attack_scale=attack_scale))


@pytest.mark.parametrize("property_index", [True, 0.5, "0"])
def test_property_index_requires_integer(property_index) -> None:
    with pytest.raises(ValueError, match="property_index must be a non-negative integer"):
        VerificationEngine().verify(VerificationRequest("battery", property_index=property_index))


@pytest.mark.parametrize("max_generators", [True, -1, 1.5, "50"])
def test_max_generators_requires_positive_integer(max_generators) -> None:
    with pytest.raises(ValueError, match="max_generators must be a positive integer"):
        VerificationEngine().verify(VerificationRequest("battery", max_generators=max_generators))


@pytest.mark.parametrize("domain", ["", "   ", None, 123])
def test_domain_requires_non_empty_string(domain) -> None:
    with pytest.raises(ValueError, match="domain must be a non-empty string"):
        VerificationEngine().verify(VerificationRequest(domain=domain))
