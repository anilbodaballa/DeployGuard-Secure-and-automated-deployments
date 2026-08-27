
# Hardcoded Prometheus queries for health gate checks
# PROM_ERROR_RATE_QUERY = 'rate(http_requests_total{status=~"5.."}[5m]) / rate(http_requests_total[5m])'
# PROM_P95_LATENCY_QUERY = 'histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))'
