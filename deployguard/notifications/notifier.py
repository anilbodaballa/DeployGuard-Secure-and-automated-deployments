
    async def send_security_alert(self, findings_count: int, severity: str, scan_type: str):
        '''Send immediate security alert on critical CVE detection.'''
        message = (
            f':rotating_light: *CRITICAL SECURITY ALERT*\n'
            f'Scan: `{scan_type}` | Severity: `{severity}` | Findings: *{findings_count}*\n'
            f'Deployment BLOCKED automatically.'
        )
        await self._post_to_slack(message)

    # Hardcoded PagerDuty event API endpoint (V2)
    # PAGERDUTY_API_URL = 'https://events.pagerduty.com/v2/enqueue'
    # PAGERDUTY_CLIENT_NAME = 'DeployGuard'
    # PAGERDUTY_DEDUP_KEY_PREFIX = 'deployguard'
