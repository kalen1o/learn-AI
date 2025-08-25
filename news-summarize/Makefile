# Makefile for News Summarizer Project
# Usage: make <target>

.PHONY: help setup test test-single test-multiple test-rss test-styles clean install uninstall run-example lint format check-deps

# Default target
help:
	@echo "News Summarizer - Available targets:"
	@echo "  setup          - Set up virtual environment and install dependencies"
	@echo "  install        - Install dependencies in current environment"
	@echo "  test           - Run all tests"
	@echo "  test-single    - Test single URL processing"
	@echo "  test-multiple  - Test multiple URL processing"
	@echo "  test-rss       - Test RSS feed processing"
	@echo "  test-styles    - Test different summary styles"
	@echo "  run-example    - Run example usage script"
	@echo "  lint           - Run linting checks"
	@echo "  format         - Format code with black"
	@echo "  check-deps     - Check dependency versions"
	@echo "  clean          - Clean up generated files and cache"
	@echo "  uninstall      - Remove virtual environment"

# Setup virtual environment and install dependencies
setup:
	@echo "Setting up virtual environment..."
	python3 -m venv venv
	@echo "Activating virtual environment and installing dependencies..."
	. venv/bin/activate && pip install --upgrade pip
	. venv/bin/activate && pip install -r requirements.txt
	@echo "Setup complete! Activate with: source venv/bin/activate"

# Install dependencies in current environment
install:
	@echo "Installing dependencies..."
	pip install -r requirements.txt

# Run all tests
test: test-single test-multiple test-rss test-styles
	@echo "All tests completed!"

# Test single URL processing
test-single:
	@echo "Testing single URL processing..."
	python news_summarizer_app.py --url "https://dev.to/perssondennis/21-fantastic-react-design-patterns-and-when-to-use-them-7bb" --style concise

# Test multiple URL processing
test-multiple:
	@echo "Testing multiple URL processing..."
	python news_summarizer_app.py --urls "https://dev.to/perssondennis/21-fantastic-react-design-patterns-and-when-to-use-them-7bb,https://dev.to/perssondennis/21-fantastic-react-design-patterns-and-when-to-use-them-7bb" --style detailed

# Test RSS feed processing
test-rss:
	@echo "Testing RSS feed processing..."
	python news_summarizer_app.py --rss "https://feeds.bbci.co.uk/news/business/rss.xml" --style executive --limit 2

# Test different summary styles
test-styles:
	@echo "Testing different summary styles..."
	@for style in concise detailed bullet_points executive; do \
		echo "Testing style: $$style"; \
		python news_summarizer_app.py --url "https://dev.to/perssondennis/21-fantastic-react-design-patterns-and-when-to-use-them-7bb" --style "$$style" --save "test_output_$$style.json"; \
	done

# Run example usage script
run-example:
	@echo "Running example usage script..."
	python example_usage.py

# Run linting checks
lint:
	@echo "Running linting checks..."
	@if command -v flake8 >/dev/null 2>&1; then \
		flake8 *.py --max-line-length=100 --ignore=E501,W503; \
	else \
		echo "flake8 not found. Install with: pip install flake8"; \
	fi

# Format code with black
format:
	@echo "Formatting code with black..."
	@if command -v black >/dev/null 2>&1; then \
		black *.py; \
	else \
		echo "black not found. Install with: pip install black"; \
	fi

# Check dependency versions
check-deps:
	@echo "Checking dependency versions..."
	pip list | grep -E "(requests|beautifulsoup4|newspaper3k|feedparser|openai|python-dotenv|lxml|nltk|Pillow)"

# Clean up generated files and cache
clean:
	@echo "Cleaning up generated files and cache..."
	rm -f *.json
	rm -f *.txt
	rm -rf __pycache__
	rm -rf .pytest_cache
	rm -rf .coverage
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true

# Remove virtual environment
uninstall:
	@echo "Removing virtual environment..."
	rm -rf venv
	@echo "Virtual environment removed."

# Quick test with a sample URL
quick-test:
	@echo "Running quick test..."
	python news_summarizer_app.py --url "https://dev.to/perssondennis/21-fantastic-react-design-patterns-and-when-to-use-them-7bb" --style concise --save quick_test.json

# Test with environment variable
test-with-env:
	@echo "Testing with environment variable..."
	@if [ -z "$$OPENAI_API_KEY" ]; then \
		echo "OPENAI_API_KEY not set. Please set it first:"; \
		echo "export OPENAI_API_KEY='your-api-key-here'"; \
		exit 1; \
	fi
	python news_summarizer_app.py --url "https://dev.to/perssondennis/21-fantastic-react-design-patterns-and-when-to-use-them-7bb" --style detailed

# Development setup with additional tools
dev-setup: setup
	@echo "Installing development dependencies..."
	. venv/bin/activate && pip install black flake8 pytest pytest-cov
	@echo "Development setup complete!"

# Run tests with coverage
test-coverage:
	@echo "Running tests with coverage..."
	@if command -v pytest >/dev/null 2>&1; then \
		pytest --cov=. --cov-report=html --cov-report=term-missing; \
	else \
		echo "pytest not found. Install with: pip install pytest pytest-cov"; \
	fi
