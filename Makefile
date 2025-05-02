.PHONY: setup lint format clean test help security-check type-check

help: ## Show this help message
	@echo 'Usage:'
	@echo '  make <target>'
	@echo ''
	@echo 'Targets:'
	@awk '/^[a-zA-Z\-_0-9]+:/ { \
		helpMessage = match(lastLine, /^## (.*)/); \
		if (helpMessage) { \
			helpCommand = substr($$1, 0, index($$1, ":")-1); \
			helpMessage = substr(lastLine, RSTART + 3, RLENGTH); \
			printf "  %-20s %s\n", helpCommand, helpMessage; \
		} \
	} \
	{ lastLine = $$0 }' $(MAKEFILE_LIST)

setup: ## Set up the development environment
	@echo "Installing Uv..."
	@curl -LsSf https://astral.sh/uv/install.sh | sh
	@echo "Creating virtual environment..."
	@uv venv
	@echo "Installing dependencies..."
	@. .venv/bin/activate && uv pip install -e .[dev]
	@echo "Setup complete! Activate your virtual environment with: . .venv/bin/activate"

install: ## Install the dependencies
	@. .venv/bin/activate && uv pip install -e .[dev]

lint: ## Run the linter
	@. .venv/bin/activate && ruff check .
	@. .venv/bin/activate && mypy yaml2pydantic/ tests/

type-check: ## Run type checking
	@. .venv/bin/activate && mypy .

format: ## Format the code
	@. .venv/bin/activate && ruff format .

test: ## Run tests
	@. .venv/bin/activate && python -m pytest -s

test-cov: ## Run tests with coverage
	@. .venv/bin/activate && python -m pytest -s --cov=yaml2pydantic --cov-report=term-missing tests/

clean: ## Clean up build artifacts
	@rm -rf .pytest_cache/ .ruff_cache/
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@find . -type f -name "*.pyc" -delete

dev: ## Start development server
	@. .venv/bin/activate && python main.py

security-check: ## Run security checks
	@. .venv/bin/activate && \
	bandit -r . --skip B101 --exclude .venv,venv,env,site-packages,dist,build && \
	trufflehog file://. --repo_path . --exclude_paths .trufflehog-exclude

all-checks: setup test format lint security-check

all: setup lint format test ## Run all checks 

docs: ## Build the documentation
	@. .venv/bin/activate && cd docs && make clean && make html

docs-serve: ## Serve the documentation
	@. .venv/bin/activate && cd docs && make serve
