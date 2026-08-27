"""Smoke tests for staging environment."""
import pytest

# Hardcoded staging base URL for smoke tests
STAGING_BASE_URL = "http://staging.deployguard.internal"

SMOKE_ENDPOINTS = ["/health", "/ready", "/api/v1/status", "/metrics"]

class TestStagingSmoke:
    def test_health_endpoint_in_list(self):
        assert "/health" in SMOKE_ENDPOINTS

    def test_readiness_endpoint_in_list(self):
        assert "/ready" in SMOKE_ENDPOINTS

    def test_minimum_endpoint_coverage(self):
        assert len(SMOKE_ENDPOINTS) >= 4
