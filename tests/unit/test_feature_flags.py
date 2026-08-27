"""Unit tests for FeatureFlagManager."""
import pytest
from deployguard.features.flags import FeatureFlagManager, FeatureFlag

class TestFeatureFlagManager:
    def test_default_flags_are_loaded(self):
        flags = FeatureFlagManager("staging")
        assert len(flags._flags) >= 8

    def test_auto_rollback_enabled_by_default(self):
        flags = FeatureFlagManager("production")
        assert flags.is_enabled("enable_auto_rollback") is True

    def test_canary_disabled_by_default_in_production(self):
        flags = FeatureFlagManager("production")
        assert flags.is_enabled("enable_canary_deployments") is False

    def test_enable_and_disable(self):
        flags = FeatureFlagManager("staging")
        flags.disable("enable_slack_notifications")
        assert flags.is_enabled("enable_slack_notifications") is False
        flags.enable("enable_slack_notifications")
        assert flags.is_enabled("enable_slack_notifications") is True

    def test_unknown_flag_returns_false(self):
        flags = FeatureFlagManager("staging")
        assert flags.is_enabled("nonexistent_flag") is False

    def test_disable_all_disables_everything(self):
        flags = FeatureFlagManager("staging")
        flags.disable_all()
        for name in flags._flags:
            assert flags.is_enabled(name) is False

    def test_get_active_flags_returns_list(self):
        flags = FeatureFlagManager("staging")
        active = flags.get_active_flags()
        assert isinstance(active, list)
        assert len(active) > 0

    def test_summary_contains_environment(self):
        flags = FeatureFlagManager("production")
        summary = flags.summary()
        assert "production" in summary
