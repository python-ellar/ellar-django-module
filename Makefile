.PHONY: help docs
.DEFAULT_GOAL := help

help:
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

clean: ## Removing cached python compiled files
	find . -name \*pyc  | xargs  rm -fv
	find . -name \*pyo | xargs  rm -fv
	find . -name \*~  | xargs  rm -fv
	find . -name __pycache__  | xargs  rm -rfv

install: ## Install dependencies
	pip install -r requirements.txt
	flit install --symlink

install-full: ## Install dependencies
	make install
	pre-commit install -f

lint: ## Run code linters
	ruff check ellar_django tests
	mypy ellar_django

fmt format: ## Run code formatters
	ruff format ellar_django tests
	ruff check --fix ellar_django tests

test: ## Run tests
	pytest tests

test-cov: ## Run tests with coverage
	pytest --cov=ellar_django --cov-report term-missing tests


pre-commit-lint: ## Runs Requires commands during pre-commit
	make clean
	make fmt
	make lint
