"""Tests for core entity models."""
import pytest
from src.models.entities import (
    AuthorizationGrant, AuthorizationMode, Finding,
    FindingStatus, Severity, Confidence
)


def test_authorization_grant_confirmed():
    grant = AuthorizationGrant(status="CONFIRMED", mode=AuthorizationMode.PASSIVE)
    assert grant.is_confirmed is True
    assert grant.allows_active_testing is False


def test_authorization_grant_not_confirmed():
    grant = AuthorizationGrant(status="PENDING")
    assert grant.is_confirmed is False


def test_authorization_grant_active():
    grant = AuthorizationGrant(status="CONFIRMED", mode=AuthorizationMode.ACTIVE_STAGING)
    assert grant.allows_active_testing is True


def test_severity_enum_values():
    assert Severity.CRITICAL.value == "Critical"
    assert Severity.HIGH.value == "High"
    assert Severity.INFO.value == "Info"


def test_finding_status_values():
    assert FindingStatus.CONFIRMED.value == "confirmed"
    assert FindingStatus.REVIEW_GAP.value == "review-gap"
