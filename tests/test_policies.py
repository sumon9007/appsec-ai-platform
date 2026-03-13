"""Tests for authorization policy enforcement."""
import pytest
from src.models.entities import AuthorizationGrant, AuthorizationMode
from src.policies.authorization import AuthorizationError, require_active_testing, require_confirmed


def test_require_confirmed_passes():
    grant = AuthorizationGrant(status="CONFIRMED")
    require_confirmed(grant)  # Should not raise


def test_require_confirmed_raises_on_pending():
    grant = AuthorizationGrant(status="PENDING")
    with pytest.raises(AuthorizationError, match="AUTHORIZATION REQUIRED"):
        require_confirmed(grant)


def test_require_active_testing_raises_on_passive():
    grant = AuthorizationGrant(status="CONFIRMED", mode=AuthorizationMode.PASSIVE)
    with pytest.raises(AuthorizationError, match="ACTIVE TESTING NOT AUTHORIZED"):
        require_active_testing(grant)


def test_require_active_testing_passes_on_staging():
    grant = AuthorizationGrant(status="CONFIRMED", mode=AuthorizationMode.ACTIVE_STAGING)
    require_active_testing(grant)  # Should not raise
