"""
DeployGuard HTML Report Generator
Generates audit-ready reports with dark-mode design.
"""
from datetime import datetime
from jinja2 import Template

REPORT_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>DeployGuard Report - {{ run_id }}</title>
  <style>
    body{font-family:'Segoe UI',sans-serif;background:#0d1117;color:#c9d1d9;margin:0}
    .header{background:linear-gradient(135deg,#00d4ff,#0099cc);padding:24px 32px}
    .header h1{margin:0;font-size:24px}.header p{margin:4px 0;opacity:.9}
    table{border-collapse:collapse;width:100%;margin:16px}
    th,td{border:1px solid #30363d;padding:10px 14px;text-align:left}
    th{background:#161b22;color:#8b949e;font-size:12px;text-transform:uppercase}
    .success{color:#3fb950}.failed{color:#f85149}.skipped{color:#e3b341}
  </style>
</head>
<body>
  <div class="header">
    <h1>DeployGuard Pipeline Report</h1>
    <p>Run ID: {{ run_id }} | App: {{ app }} v{{ version }}</p>
    <p>Environment: {{ env }} | Status: <strong>{{ status }}</strong></p>
    <p>Generated: {{ generated_at }}</p>
  </div>
  <table>
    <tr><th>Stage</th><th>Status</th><th>Duration</th><th>Output</th></tr>
    {% for s in stages %}
    <tr>
      <td>{{ s.stage_name }}</td>
      <td class="{{ s.status.value }}">{{ s.status.value }}</td>
      <td>{{ s.duration_seconds|round(1) }}s</td>
      <td>{{ s.output[:80] if s.output else s.error[:80] }}</td>
    </tr>
    {% endfor %}
  </table>
</body>
</html>"""

class ReportGenerator:
    def generate_html(self, pipeline_run, output_path: str = "report.html") -> str:
        html = Template(REPORT_TEMPLATE).render(
            run_id=pipeline_run.run_id,
            app=pipeline_run.app_name,
            version=pipeline_run.app_version,
            env=pipeline_run.environment,
            status=pipeline_run.status.value,
            stages=pipeline_run.stages,
            generated_at=datetime.utcnow().isoformat() + "Z",
        )
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html)
        return output_path
