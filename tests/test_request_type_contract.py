import pytest

from cpsverify.engine import VerificationEngine, VerificationRequest


@pytest.mark.parametrize("invalid_method", [None, 1, [], {}, True, 1.5])
def test_invalid_method_types_raise_value_error(invalid_method):
    with pytest.raises(ValueError, match="method"):
        VerificationEngine().verify(VerificationRequest("battery", method=invalid_method))


@pytest.mark.parametrize("invalid_request", [None, {}, "battery", 1])
def test_invalid_request_object_is_rejected(invalid_request):
    with pytest.raises(ValueError, match="VerificationRequest"):
        VerificationEngine().verify(invalid_request)
