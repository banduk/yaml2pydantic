.PHONY: setup lint format build clean test help

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
	@source .venv/bin/activate && uv pip install -e .[dev]
	@echo "Installing Hatch..."
	@source .venv/bin/activate && uv pip install hatch
	@echo "Setup complete! Activate your virtual environment with: source .venv/bin/activate"

install: ## Install the dependencies
	@source .venv/bin/activate && uv pip install -e .[dev]

lint: ## Run the linter
	@source .venv/bin/activate && ruff check .

lint-fix: ## Run the linter and fix the issues
	@source .venv/bin/activate && ruff check --fix .

format: ## Format the code
	@source .venv/bin/activate && ruff format .

build: ## Build the project
	@source .venv/bin/activate && hatch build

test: ## Run tests
	@source .venv/bin/activate && python -m pytest

clean: ## Clean up build artifacts
	@rm -rf build/ dist/ *.egg-info/ .pytest_cache/ .ruff_cache/
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@find . -type f -name "*.pyc" -delete

dev: ## Start development server
	@source .venv/bin/activate && python main.py

all: setup lint format build test ## Run all checks and build 