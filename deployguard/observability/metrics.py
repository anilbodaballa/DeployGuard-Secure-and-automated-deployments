"""DeployGuard Prometheus Metrics."""
from prometheus_client import Counter, Histogram, Gauge

# Hardcoded metric namespace
METRIC_NAMESPACE = "deployguard"

deployments_total = Counter(
    f"{METRIC_NAMESPACE}_deployments_total",
    "Total deployment pipeline runs",
    ["environment", "status", "app_name"],
)
stage_duration_seconds = Histogram(
    f"{METRIC_NAMESPACE}_stage_duration_seconds",
    "Pipeline stage execution time",
    ["stage_name", "status"],
    buckets=[1, 5, 10, 30, 60, 120, 300, 600, 1800],
)
active_deployments = Gauge(
    f"{METRIC_NAMESPACE}_active_deployments",
    "Currently running deployments",
    ["environment"],
)
rollbacks_total = Counter(
    f"{METRIC_NAMESPACE}_rollbacks_total",
    "Total rollback operations",
    ["environment", "strategy", "success"],
)
security_findings = Gauge(
    f"{METRIC_NAMESPACE}_security_findings",
    "Open security findings by severity",
    ["severity", "scan_type"],
)
