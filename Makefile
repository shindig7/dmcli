###########
# GLOBALS #
###########
PROJECT_NAME = src # replace this with project folder
PYTHON_INTERPRETER = python

ISORT = isort $(PROJECT_NAME) tests
BLACK = black --target-version py38 $(PROJECT_NAME) tests
SHELL := /bin/bash

#########################
# PROJECT SPECIFIC VARS #
#########################

############
# COMMANDS #
############
.PHONY: help
help:
	@echo "format - automatically reformat code"
	@echo "lint - check style"
	@echo "test - run all tests"
	@echo "coverage - run all tests and serve coverage report"
	@echo "clean - remove all build, test, coverage, and Python artifacts"
	@echo "run - perform the operations of the project with the set configuration"

.PHONY: format
format:
	$(ISORT)
	$(BLACK)

.PHONY: lint
lint: format
	-flake8 $(PROJECT_NAME) tests/

.PHONY: test
test:
	pytest tests/

.PHONY: coverage
coverage:
	pytest --cov=$(PROJECT_NAME) tests/

.PHONY: coverage-report
coverage-report:
	pytest --cov=$(PROJECT_NAME) tests/
	@echo "building coverage html"
	@coverage html
	cd htmlcov && python -m http.server 1080

.PHONY: clean
clean:
	find . -mount -type f -name "*.py[co]" -delete
	find . -mount -type d -name "__pycache__" -delete
	find . -mount -type d -name "site" -exec rm -rf {} +
	find . -mount -type d -name ".ipynb_checkpoints" -exec rm -rf {} +
	find . -mount -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -mount -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -mount -type d -name "htmlcov" -exec rm -rf {} +

.PHONY: run
run:
	python -m $(PROJECT_NAME)
