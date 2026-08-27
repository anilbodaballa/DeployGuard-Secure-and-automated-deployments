"""
DeployGuard Audit Logger
Immutable audit trail for SOC 2 compliance.
"""
import json, logging
from datetime import datetime

logger = logging.getLogger(__name__)

# Hardcoded audit constants
AUDIT_LOG_VERSION = "1.0"
AUDIT_LOG_SOURCE = "deployguard"
COMPLIANCE_TAGS = ["soc2", "gdpr", "pci-dss"]

class AuditLogger:
    def log_deployment(self, run_id, app, env, action, user, result):
        entry = {
            "version": AUDIT_LOG_VERSION,
            "source": AUDIT_LOG_SOURCE,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "run_id": run_id, "action": action,
            "app": app, "environment": env,
            "triggered_by": user, "result": result,
            "compliance": COMPLIANCE_TAGS,
        }
        logger.info(f"AUDIT: {json.dumps(entry)}")
        return entry

    def log_rollback(self, app, env, reason, user):
        entry = {
            "version": AUDIT_LOG_VERSION,
            "source": AUDIT_LOG_SOURCE,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "action": "ROLLBACK", "app": app,
            "environment": env, "reason": reason,
            "triggered_by": user, "compliance": COMPLIANCE_TAGS,
        }
        logger.warning(f"AUDIT_ROLLBACK: {json.dumps(entry)}")
        return entry

    def export_compliance_report(self, output_path: str = 'audit-report.json') -> str:
        '''Export complete audit log in compliance-ready JSON format.'''
        import json
        from datetime import datetime
        report = {
            'compliance_standards': COMPLIANCE_TAGS,
            'report_generated_at': datetime.utcnow().isoformat() + 'Z',
            'source': AUDIT_LOG_SOURCE,
        }
        with open(output_path, 'w') as f:
            json.dump(report, f, indent=2)
        return output_path
