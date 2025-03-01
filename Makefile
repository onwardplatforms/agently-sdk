.PHONY: help venv install install-dev clean test lint format check all

# Variables
PYTHON = python3
VENV = venv
VENV_BIN = $(VENV)/bin
PIP = $(VENV_BIN)/pip
PYTEST = $(VENV_BIN)/pytest
BLACK = $(VENV_BIN)/black
ISORT = $(VENV_BIN)/isort
MYPY = $(VENV_BIN)/mypy
ACTIVATE = . $(VENV)/bin/activate &&

# Directories
SRC_DIR = src
TEST_DIR = tests

help:
	@echo "Available commands:"
	@echo "  make venv        - Create virtual environment"
	@echo "  make install     - Install dependencies"
	@echo "  make clean       - Remove virtual environment and cache files"
	@echo "  make test        - Run tests with coverage"
	@echo "  make lint        - Run linters (black, isort)"
	@echo "  make format      - Format code (black, isort)"
	@echo "  make check       - Run type checking (mypy)"
	@echo "  make all         - Run all checks (format, lint, type check, test)"

venv:
	$(PYTHON) -m venv $(VENV)
	$(ACTIVATE) $(PIP) install --upgrade pip

install: venv
	$(ACTIVATE) $(PIP) install -r requirements.txt
	$(ACTIVATE) $(PIP) install -e .

clean:
	rm -rf $(VENV)
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov
	rm -rf .mypy_cache
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +

test:
	$(ACTIVATE) $(PYTEST) $(TEST_DIR)/ -v --cov=agently_sdk --cov-report=term-missing

lint:
	$(ACTIVATE) $(BLACK) --check $(SRC_DIR) $(TEST_DIR)
	$(ACTIVATE) $(ISORT) --check-only --profile black $(SRC_DIR) $(TEST_DIR)

format:
	$(ACTIVATE) $(BLACK) $(SRC_DIR) $(TEST_DIR)
	$(ACTIVATE) $(ISORT) --profile black $(SRC_DIR) $(TEST_DIR)

check:
	$(ACTIVATE) $(MYPY) $(SRC_DIR)

all: format lint check test 