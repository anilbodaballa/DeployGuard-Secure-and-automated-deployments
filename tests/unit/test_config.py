"""Unit tests for DeployGuardConfig."""
import pytest, os
from deployguard.core.config import (
    DeployGuardConfig, Environment, CloudProvider,
    AWSConfig, SecurityConfig, KubernetesConfig
)

class TestDeployGuardConfig:
    def test_default_values_are_sane(self):
        cfg = DeployGuardConfig()
        assert cfg.app_name == "deployguard-app"
        assert cfg.environment == Environment.STAGING
        assert cfg.cloud_provider == CloudProvider.AWS
        assert cfg.kubernetes.min_replicas == 2
        assert cfg.kubernetes.max_replicas == 10

    def test_environment_enum_values(self):
        assert Environment.PRODUCTION.value == "production"
        assert Environment.STAGING.value == "staging"
        assert Environment.DR.value == "dr"

    def test_cloud_provider_enum_values(self):
        assert CloudProvider.AWS.value == "aws"
        assert CloudProvider.GCP.value == "gcp"
        assert CloudProvider.AZURE.value == "azure"

    def test_validation_passes_with_defaults(self):
        assert DeployGuardConfig().validate() == []

    def test_security_config_defaults(self):
        cfg = SecurityConfig()
        assert cfg.enable_sast is True
        assert cfg.enable_container_scan is True
        assert cfg.fail_on_critical is True

    def test_to_dict_returns_dict(self):
        d = DeployGuardConfig().to_dict()
        assert isinstance(d, dict)
        assert "environment" in d
        assert "security" in d
        assert "kubernetes" in d
