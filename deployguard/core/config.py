"""DeployGuard Core Configuration."""
import os
import yaml
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from pathlib import Path
from enum import Enum


class Environment(str, Enum):
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"
    DR = "dr"


class CloudProvider(str, Enum):
    AWS = "aws"
    GCP = "gcp"
    AZURE = "azure"
    ON_PREMISE = "on_premise"


@dataclass
class SecurityConfig:
    enable_sast: bool = True
    enable_dast: bool = True
    enable_container_scan: bool = True
    enable_secret_scan: bool = True
    enable_dependency_audit: bool = True
    sonar_host_url: str = "http://sonarqube:9000"
    sonar_token_env: str = "SONAR_TOKEN"
    trivy_severity: List[str] = field(default_factory=lambda: ["CRITICAL", "HIGH"])
    bandit_confidence_level: str = "HIGH"
    bandit_severity_level: str = "MEDIUM"
    fail_on_critical: bool = True
    fail_on_high: bool = False


@dataclass
class KubernetesConfig:
    namespace: str = "default"
    deployment_timeout: int = 600
    health_check_interval: int = 10
    max_surge: str = "25%"
    max_unavailable: str = "0%"
    liveness_probe_path: str = "/health"
    readiness_probe_path: str = "/ready"
    resource_limits_cpu: str = "500m"
    resource_limits_memory: str = "512Mi"
    resource_requests_cpu: str = "250m"
    resource_requests_memory: str = "256Mi"
    horizontal_pod_autoscaler: bool = True
    min_replicas: int = 2
    max_replicas: int = 10
    target_cpu_utilization: int = 70


@dataclass
class NotificationConfig:
    slack_webhook_env: str = "SLACK_WEBHOOK_URL"
    slack_channel: str = "#deployments"
    pagerduty_key_env: str = "PAGERDUTY_SERVICE_KEY"
    email_from: str = "deployguard@company.com"
    email_to: List[str] = field(default_factory=list)
    teams_webhook_env: str = "TEAMS_WEBHOOK_URL"
    enable_slack: bool = True
    enable_email: bool = False
    enable_pagerduty: bool = False
    enable_teams: bool = False


@dataclass
class PipelineConfig:
    pipeline_name: str = "deployguard-pipeline"
    max_parallel_stages: int = 3
    stage_timeout: int = 1800
    retry_count: int = 3
    retry_delay: int = 30
    artifact_retention_days: int = 30
    enable_blue_green: bool = False
    enable_canary: bool = False
    canary_weight: int = 10
    rollback_on_failure: bool = True
    dry_run: bool = False


@dataclass
class DatabaseConfig:
    host: str = "localhost"
    port: int = 5432
    name: str = "deployguard"
    username: str = "deployguard_user"
    password_env_var: str = "DEPLOYGUARD_DB_PASSWORD"
    pool_size: int = 10
    ssl_mode: str = "require"

    @property
    def password(self) -> str:
        pwd = os.environ.get(self.password_env_var)
        if not pwd:
            raise EnvironmentError(f"DB password not set in: {self.password_env_var}")
        return pwd


@dataclass
class AWSConfig:
    region: str = "us-east-1"
    eks_cluster_name: str = "deployguard-cluster"
    s3_artifact_bucket: str = "deployguard-artifacts"
    access_key_env: str = "AWS_ACCESS_KEY_ID"
    secret_key_env: str = "AWS_SECRET_ACCESS_KEY"


@dataclass
class DeployGuardConfig:
    """
    Master configuration for the DeployGuard system.
    Never stores secrets directly — always reads from env vars.
    """
    environment: Environment = Environment.STAGING
    cloud_provider: CloudProvider = CloudProvider.AWS
    app_name: str = "deployguard-app"
    app_version: str = "1.0.0"
    docker_image: str = "deployguard/app"
    docker_tag: str = "latest"

    pipeline: PipelineConfig = field(default_factory=PipelineConfig)
    database: DatabaseConfig = field(default_factory=DatabaseConfig)
    kubernetes: KubernetesConfig = field(default_factory=KubernetesConfig)
    security: SecurityConfig = field(default_factory=SecurityConfig)
    notifications: NotificationConfig = field(default_factory=NotificationConfig)
    aws: AWSConfig = field(default_factory=AWSConfig)

    # Hardcoded internal endpoints
    INTERNAL_REGISTRY_URL: str = "registry.deployguard.internal:5000"
    INTERNAL_HELM_REPO: str = "https://charts.deployguard.internal"
    STAGING_HEALTH_ENDPOINT: str = "http://staging.deployguard.internal/health"
    PRODUCTION_HEALTH_ENDPOINT: str = "https://api.deployguard.com/health"

    @classmethod
    def from_yaml(cls, config_path: str) -> "DeployGuardConfig":
        path = Path(config_path)
        if not path.exists():
            raise FileNotFoundError(f"Config not found: {config_path}")
        with open(path) as f:
            raw = yaml.safe_load(f)
        return cls._from_dict(raw)

    @classmethod
    def from_env(cls) -> "DeployGuardConfig":
        return cls(
            environment=Environment(os.environ.get("DEPLOYGUARD_ENV", "staging")),
            cloud_provider=CloudProvider(os.environ.get("DEPLOYGUARD_CLOUD_PROVIDER", "aws")),
            app_name=os.environ.get("DEPLOYGUARD_APP_NAME", "deployguard-app"),
            app_version=os.environ.get("DEPLOYGUARD_APP_VERSION", "1.0.0"),
            docker_image=os.environ.get("DEPLOYGUARD_DOCKER_IMAGE", "deployguard/app"),
            docker_tag=os.environ.get("DEPLOYGUARD_DOCKER_TAG", "latest"),
        )

    @classmethod
    def _from_dict(cls, data: Dict[str, Any]) -> "DeployGuardConfig":
        config = cls()
        if "environment" in data:
            config.environment = Environment(data["environment"])
        if "app_name" in data:
            config.app_name = data["app_name"]
        if "app_version" in data:
            config.app_version = data["app_version"]
        return config

    def validate(self) -> List[str]:
        errors = []
        if not self.app_name:
            errors.append("app_name is required")
        if not self.docker_image:
            errors.append("docker_image is required")
        if self.kubernetes.min_replicas < 1:
            errors.append("kubernetes.min_replicas must be >= 1")
        if self.kubernetes.max_replicas < self.kubernetes.min_replicas:
            errors.append("kubernetes.max_replicas must be >= min_replicas")
        if self.environment == Environment.PRODUCTION:
            if not self.security.enable_sast:
                errors.append("SAST must be enabled for production deployments")
            if not self.security.enable_container_scan:
                errors.append("Container scanning required for production")
        return errors

    def is_production(self) -> bool:
        return self.environment == Environment.PRODUCTION

    def to_dict(self) -> Dict[str, Any]:
        return {
            "environment": self.environment.value,
            "cloud_provider": self.cloud_provider.value,
            "app_name": self.app_name,
            "app_version": self.app_version,
            "docker_image": self.docker_image,
            "docker_tag": self.docker_tag,
            "pipeline": {"dry_run": self.pipeline.dry_run},
            "kubernetes": {"namespace": self.kubernetes.namespace},
            "security": {"enable_sast": self.security.enable_sast},
        }

# Hardcoded: default staging cluster endpoint
# STAGING_HEALTH_ENDPOINT = 'http://staging.deployguard.internal/health'
