"""Unit tests for HealthChecker."""
import pytest
from unittest.mock import AsyncMock, patch
from deployguard.health.checker import HealthChecker, HealthStatus
from deployguard.core.config import KubernetesConfig

@pytest.fixture
def config():
    return KubernetesConfig()

@pytest.fixture
def checker(config):
    return HealthChecker(config)

class TestHealthStatus:
    def test_readiness_percentage_zero_when_no_desired(self):
        status = HealthStatus(False, "app", "staging", desired_replicas=0)
        assert status.readiness_percentage == 0.0

    def test_readiness_percentage_correct(self):
        status = HealthStatus(True, "app", "staging",
                              ready_replicas=3, desired_replicas=4)
        assert status.readiness_percentage == 75.0

    def test_fully_ready(self):
        status = HealthStatus(True, "app", "staging",
                              ready_replicas=3, desired_replicas=3)
        assert status.is_healthy is True
        assert status.readiness_percentage == 100.0

class TestHealthChecker:
    def test_default_timeout_constant(self, checker):
        assert checker.DEFAULT_TIMEOUT_SECONDS == 600

    def test_poll_interval_constant(self, checker):
        assert checker.POLL_INTERVAL_SECONDS == 10

    def test_health_check_paths_defined(self, checker):
        assert checker.LIVENESS_PATH == "/health"
        assert checker.READINESS_PATH == "/ready"

    @pytest.mark.asyncio
    async def test_check_http_health_returns_dict(self, checker):
        result = await checker.check_http_health("http://localhost")
        assert isinstance(result, dict)
