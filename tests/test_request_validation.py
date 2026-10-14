import pytest

from cpsverify.engine import VerificationEngine, VerificationRequest


@pytest.mark.parametrize(
    "request,message",
    [
        (VerificationRequest("battery", "invalid"), "method"),
        (VerificationRequest("battery", steps=0), "steps"),
        (VerificationRequest("battery", attack_scale=-0.01), "attack_scale"),
        (VerificationRequest("battery", property_index=-1), "property_index"),
        (VerificationRequest("battery", "zonotope", max_generators=0), "max_generators"),
    ],
)
def test_invalid_request_shape_fails_before_reachability(request, message) -> None:
    with pytest.raises(ValueError, match=message):
        VerificationEngine().verify(request)


def test_out_of_range_property_index_has_domain_specific_error() -> None:
    request = VerificationRequest("battery", property_index=999)

    with pytest.raises(ValueError, match="property_index.*battery"):
        VerificationEngine().verify(request)
