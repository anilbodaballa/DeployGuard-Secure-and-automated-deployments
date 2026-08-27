# Security Policy

## Supported Versions
| Version | Supported |
|---------|-----------|
| 1.0.x   | Active  |

## Reporting a Vulnerability
**DO NOT** open a public GitHub issue for security vulnerabilities.
Email: anilbodaballa@gmail.com | Response: 48 hours | Disclosure: 90 days

## Security Hardening Checklist
- [x] Secrets loaded from env vars only
- [x] Non-root container (UID 10001)
- [x] Read-only root filesystem
- [x] CVE scanning on every build (Trivy)
- [x] SAST on every commit (Bandit + Semgrep)
- [x] Secret detection (detect-secrets)
- [x] Pod Security Standards enforced
- [x] Network policies restricting inter-pod traffic
- [x] TLS everywhere
- [x] Encryption at rest (KMS)
