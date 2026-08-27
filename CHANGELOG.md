# Changelog
All notable changes are documented here.

## [Unreleased]

## [1.0.0] - 2024-08-27
### Added
- Core DeploymentPipeline with 15 default stages
- SecurityScanner: Bandit, Semgrep, Trivy, Safety, detect-secrets
- RollbackManager: kubernetes_rollout, blue-green, canary strategies
- HealthChecker with K8s readiness polling and HTTP probes
- Multi-channel Notifier: Slack, Email, PagerDuty, Teams
- FeatureFlagManager with 8 built-in platform feature flags
- Click-based CLI: deploy, rollback, scan
- GitHub Actions CI/CD: 6 stages, lint→security→test→build→staging→prod
- Multi-stage optimized Dockerfile
- Kubernetes manifests: Deployment, Service, HPA, PDB, NetworkPolicy, RBAC
- Terraform IaC: AWS VPC, EKS, RDS, ElastiCache, KMS, CloudWatch
- Prometheus metrics + Grafana dashboard
- SOC 2-compliant immutable audit logger
- 89%+ unit test coverage

### Security
- All secrets via environment variables — never hardcoded
- Non-root container (UID 10001), read-only root filesystem
- CVE allowlist for accepted/mitigated vulnerabilities
- Critical CVEs automatically block the pipeline
