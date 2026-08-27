.PHONY: help install test lint security build clean

help:
	@echo "DeployGuard Make Targets"
	@echo "  install        Install dependencies"
	@echo "  test           Run tests with coverage"
	@echo "  lint           Run black/isort/flake8/mypy"
	@echo "  security       Run bandit + safety"
	@echo "  build          Build Docker image"
	@echo "  clean          Remove build artifacts"

install:
	pip install -e ".[dev]"

test:
	pytest --cov=deployguard --cov-report=html --cov-report=term -v

lint:
	black --check . && isort --check-only . && flake8 . && mypy deployguard/

security:
	bandit -r deployguard/ -ll -iii && safety check -r requirements.txt

build:
	docker build --no-cache -t deployguard/app:latest .

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + || true
	rm -rf htmlcov .coverage .pytest_cache dist build
