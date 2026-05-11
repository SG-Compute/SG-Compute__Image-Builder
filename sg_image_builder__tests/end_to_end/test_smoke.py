"""M0 placeholder. Real E2E tests land in M5 (first spec on real AWS)."""

import os

import pytest


@pytest.mark.e2e
@pytest.mark.skipif(not os.getenv('SGI_E2E_ENABLED'), reason='SGI_E2E_ENABLED not set')
def test_placeholder_passes() -> None:
    assert True
