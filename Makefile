.PHONY: help venv install install-dev clean test lint format check all version autofix

# Variables
PYTHON = $(shell pyenv which python3)
VENV = venv
VENV_BIN = $(VENV)/bin
PIP = $(VENV_BIN)/pip
PYTEST = $(VENV_BIN)/pytest
BLACK = $(VENV_BIN)/black
ISORT = $(VENV_BIN)/isort
MYPY = $(VENV_BIN)/mypy
FLAKE8 = $(VENV_BIN)/flake8
AUTOFLAKE = $(VENV_BIN)/autoflake
ACTIVATE = . $(VENV)/bin/activate &&
PACKAGE_NAME = agently_sdk

# Directories
SRC_DIR = src
TEST_DIR = tests

help:
	@echo "Available commands:"
	@echo "  make venv        - Create virtual environment"
	@echo "  make install     - Install production dependencies"
	@echo "  make install-dev - Install development dependencies"
	@echo "  make clean       - Remove virtual environment and cache files"
	@echo "  make test        - Run tests with coverage"
	@echo "  make lint        - Run linters (black, isort, flake8)"
	@echo "  make format      - Format code (black, isort)"
	@echo "  make autofix     - Run autoformatters and fixers (autoflake, black, isort)"
	@echo "  make check       - Run type checking (mypy)"
	@echo "  make all         - Run all checks (format, lint, type check, test)"
	@echo "  make version V=X.Y.Z - Update version number to X.Y.Z"

venv:
	$(PYTHON) -m venv $(VENV)
	$(PYTHON) -m pip install --upgrade pip setuptools wheel

install: venv
	$(PIP) install -r requirements.txt
	$(PIP) install -e .

install-dev: install
	$(PIP) install -r dev-requirements.txt

clean:
	rm -rf $(VENV)
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov
	rm -rf .mypy_cache
	rm -rf .tox
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +

test:
	$(ACTIVATE) $(PYTEST) $(TEST_DIR)/ -v --cov=$(PACKAGE_NAME) --cov-report=term-missing --cov-report=html

lint:
	$(ACTIVATE) $(BLACK) --check $(SRC_DIR)
	$(ACTIVATE) $(ISORT) --check-only --profile black $(SRC_DIR)
	$(ACTIVATE) $(FLAKE8) $(SRC_DIR)

format:
	$(ACTIVATE) $(BLACK) $(SRC_DIR)
	$(ACTIVATE) $(ISORT) --profile black $(SRC_DIR)

autofix:
	@echo "Running autoflake..."
	$(ACTIVATE) $(AUTOFLAKE) --remove-all-unused-imports --recursive --remove-unused-variables --in-place $(SRC_DIR)
	@echo "Running black..."
	$(ACTIVATE) $(BLACK) $(SRC_DIR)
	@echo "Running isort..."
	$(ACTIVATE) $(ISORT) --profile black $(SRC_DIR)
	@echo "Running flake8..."
	$(ACTIVATE) $(FLAKE8) $(SRC_DIR) || true
	@echo "Autofix complete!"

check:
	$(ACTIVATE) $(MYPY) $(SRC_DIR)

all: format lint check test

version:
	@if [ -z "$(V)" ]; then \
		echo "Error: Version not specified. Use 'make version V=X.Y.Z'"; \
		exit 1; \
	fi
	@echo "Updating version to $(V)"
	@python scripts/update_version.py $(V)
	@echo "Version updated. Don't forget to commit the changes." 