"""Unit tests for RollbackManager."""
import pytest
from unittest.mock import AsyncMock, patch
from deployguard.rollback.manager import RollbackManager, RollbackStrategy, RollbackRecord
from deployguard.core.config import DeployGuardConfig

@pytest.fixture
def config():
    return DeployGuardConfig()

@pytest.fixture
def manager(config):
    return RollbackManager(config)

class TestRollbackManager:
    def test_version_tracking(self, manager):
        manager.track_version("staging", "1.2.3")
        assert manager._current_versions.get("staging") == "1.2.3"

    def test_rollback_history_is_empty_initially(self, manager):
        assert manager.get_rollback_history() == []

    def test_get_last_rollback_none_when_empty(self, manager):
        assert manager.get_last_rollback() is None

    def test_rollback_record_to_dict(self):
        from datetime import datetime
        record = RollbackRecord(
            rollback_id="test-01",
            triggered_at=datetime.utcnow(),
            triggered_by="ci",
            reason="test",
            strategy=RollbackStrategy.KUBERNETES_ROLLOUT,
            from_version="2.0.0",
            to_version="1.9.0",
            namespace="staging",
            app_name="myapp",
        )
        d = record.to_dict()
        assert d["rollback_id"] == "test-01"
        assert d["strategy"] == "kubernetes_rollout"
        assert d["success"] is False
