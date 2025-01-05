.PHONY: build clean test lint run preview install fmt fmt-check deps all dry-run run-verbose

# Python parameters
PYTHON=python3
PIP=pip3
POETRY=poetry
BINARY_NAME=backup-home

# Default rclone remote and path
RCLONE_REMOTE ?= drive_Crypt

# Detect OS for path construction
ifdef COMSPEC
    # Windows path (COMSPEC is set on Windows)
    RCLONE_PATH ?= Machines/$(shell hostname)/Users/$(shell echo %USERNAME%)
else
    # Unix-like systems (Linux/macOS)
    RCLONE_PATH ?= Machines/$(shell hostname)/$(shell basename $(shell dirname $(HOME)))/$(shell whoami)
endif

# Default target
all: clean install

# Install the project
install:
	$(POETRY) install

# Clean build files
clean:
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf __pycache__/
	rm -rf .pytest_cache/
	find . -type d -name __pycache__ -exec rm -r {} +
	find . -type f -name "*.pyc" -delete

# Run tests
test:
	$(POETRY) run pytest

# Run linting
lint:
	$(POETRY) run ruff check .

# Format code
fmt:
	$(POETRY) run ruff format .

# Check code formatting
fmt-check:
	$(POETRY) run ruff format --check .

# Install dependencies
deps:
	$(POETRY) install

# Build distribution
build:
	$(POETRY) build

# Run the program with default options
run:
	$(POETRY) run $(BINARY_NAME) \
		--source $(HOME) \
		"$(RCLONE_REMOTE):$(RCLONE_PATH)"

# Preview what would be done without actually doing it
preview:
	$(POETRY) run $(BINARY_NAME) \
		--source $(HOME) \
		"$(RCLONE_REMOTE):$(RCLONE_PATH)" \
		--preview

# Run with verbose output
run-verbose:
	$(POETRY) run $(BINARY_NAME) \
		--source $(HOME) \
		"$(RCLONE_REMOTE):$(RCLONE_PATH)" \
		-v

# Check all (format, lint, test)
check: fmt-check lint test
