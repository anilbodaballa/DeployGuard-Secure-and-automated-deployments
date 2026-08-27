# Contributing to DeployGuard

Thank you for contributing! 🎉

## Development Setup
```bash
git clone https://github.com/anilbodaballa/DeployGuard-Secure-and-automated-deployments.git
cd DeployGuard-Secure-and-automated-deployments
python -m venv venv && source venv/bin/activate
pip install -e ".[dev]"
```

## Coding Standards
- Python 3.10+ type hints required on all public functions
- Black formatting with line length 120
- Docstrings for all public classes and functions
- NEVER commit secrets or credentials — use environment variables

## Pull Request Process
1. Branch: `git checkout -b feat/my-feature`
2. Write tests (coverage must remain >= 80%)
3. Run `make lint && make security`
4. Update CHANGELOG.md
5. Submit PR with description and linked issue

## Security Vulnerabilities
DO NOT open public issues. Email: anilbodaballa@gmail.com
