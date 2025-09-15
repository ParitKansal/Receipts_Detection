# Receipt Detection System Makefile

.PHONY: help install install-dev setup test run clean lint format

help:  ## Show this help message
	@echo "Receipt Detection System"
	@echo "======================="
	@echo ""
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

install:  ## Install production dependencies
	pip install -r requirements.txt

install-dev:  ## Install development dependencies
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

setup:  ## Run setup script to verify installation
	python scripts/setup.py

test:  ## Run all tests
	python scripts/test_api.py
	python scripts/test_bbox.py
	python scripts/test_bbox_bulk.py

run:  ## Start the API server
	python app.py

run-dev:  ## Start the API server in development mode
	uvicorn app:app --host 0.0.0.0 --port 8888 --reload

clean:  ## Clean up temporary files
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .pytest_cache
	rm -rf .mypy_cache

lint:  ## Run linting
	flake8 src/ app.py config.py
	mypy src/ app.py config.py

format:  ## Format code
	black src/ app.py config.py examples/ scripts/

examples:  ## Run example scripts
	python examples/basic_usage.py
	python examples/batch_processing.py
	python examples/api_client.py

docs:  ## Generate documentation (if using sphinx)
	@echo "Documentation is available in the docs/ folder"
	@echo "Open docs/README.md for more information"

docker-build:  ## Build Docker image
	docker build -t receipt-detection .

docker-run:  ## Run Docker container
	docker run -p 8888:8888 receipt-detection

# Development workflow
dev-setup: install-dev setup  ## Complete development setup
	@echo "Development environment ready!"

# Production deployment
prod-install: install  ## Production installation
	python scripts/setup.py

# Quick start
quick-start: install setup run  ## Quick start (install, setup, run)
	@echo "System is running at http://127.0.0.1:8888"
