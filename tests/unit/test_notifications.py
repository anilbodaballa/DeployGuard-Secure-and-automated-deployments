"""Unit tests for Notifier."""
import pytest
from unittest.mock import AsyncMock, patch
from deployguard.notifications.notifier import Notifier
from deployguard.core.config import NotificationConfig

@pytest.fixture
def config():
    cfg = NotificationConfig()
    cfg.enable_slack = True
    cfg.enable_email = False
    cfg.enable_pagerduty = False
    return cfg

@pytest.fixture
def notifier(config):
    return Notifier(config)

class TestNotifier:
    def test_calculate_duration_no_times(self):
        from unittest.mock import MagicMock
        run = MagicMock()
        run.started_at = None
        run.completed_at = None
        result = Notifier._calculate_duration(run)
        assert result == "N/A"

    def test_slack_emoji_map_is_complete(self, notifier):
        for status in ["success", "failed", "rolled_back", "running", "pending"]:
            assert status in notifier.SLACK_EMOJI_MAP

    def test_slack_color_map_has_correct_colors(self, notifier):
        assert notifier.SLACK_COLOR_MAP["success"] == "#36a64f"
        assert notifier.SLACK_COLOR_MAP["failed"] == "#ff0000"

    @pytest.mark.asyncio
    async def test_send_success_does_not_raise(self, notifier):
        with patch.object(notifier, "_post_to_slack", new_callable=AsyncMock):
            await notifier.send_success("app", "1.0.0", "staging")

    @pytest.mark.asyncio
    async def test_send_failure_does_not_raise(self, notifier):
        with patch.object(notifier, "_post_to_slack", new_callable=AsyncMock):
            await notifier.send_failure("app", "1.0.0", "staging", "Error msg")
