import pytest
from openapi_spec_validator import validate
from detection.openapi import OPENAPI_SPEC

pytestmark = pytest.mark.unit


def test_openapi_spec_is_valid():
    """Validates that the generated OPENAPI_SPEC complies with the OpenAPI specification."""
    # validate() raises an exception if the spec is invalid
    validate(OPENAPI_SPEC)
