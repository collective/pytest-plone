### Defensive settings for make:
#     https://tech.davis-hansson.com/p/make/
SHELL:=bash
.ONESHELL:
.SHELLFLAGS:=-xeu -o pipefail -O inherit_errexit -c
.SILENT:
.DELETE_ON_ERROR:
MAKEFLAGS+=--warn-undefined-variables
MAKEFLAGS+=--no-builtin-rules

# We like colors
# From: https://coderwall.com/p/izxssa/colored-makefile-for-golang-projects
RED=`tput setaf 1`
GREEN=`tput setaf 2`
RESET=`tput sgr0`
YELLOW=`tput setaf 3`

# Python checks
UV?=uv

# installed?
ifeq (, $(shell which $(UV) ))
  $(error "UV=$(UV) not found in $(PATH)")
endif

BACKEND_FOLDER=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))

ifdef PLONE_VERSION
PLONE_VERSION := $(PLONE_VERSION)
else
PLONE_VERSION := 6.1.1
endif

VENV_FOLDER=$(BACKEND_FOLDER)/.venv
BIN_FOLDER=$(VENV_FOLDER)/bin

# Environment variables to be exported
export PYTHONWARNINGS := ignore
export DOCKER_BUILDKIT := 1

all: build

# Add the following 'help' target to your Makefile
# And add help text after each target name starting with '\#\#'
.PHONY: help
help: ## This help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

############################################
# Config
############################################
instance/etc/zope.ini instance/etc/zope.conf: ## Create instance configuration
	@echo "$(GREEN)==> Create instance configuration$(RESET)"
	@uvx cookiecutter -f --no-input -c 2.1.1 --config-file instance.yaml gh:plone/cookiecutter-zope-instance

.PHONY: config
config: instance/etc/zope.ini

############################################
# Install
############################################

requirements-mxdev.txt: ## Generate constraints file
	@echo "$(GREEN)==> Generate constraints file$(RESET)"
	@echo '-c https://dist.plone.org/release/$(PLONE_VERSION)/constraints.txt' > requirements.txt
	@uvx mxdev -c mx.ini

$(VENV_FOLDER): requirements-mxdev.txt ## Install dependencies
	@echo "$(GREEN)==> Install environment$(RESET)"
	@uv venv $(VENV_FOLDER)
	@uv pip install -r requirements-mxdev.txt

.PHONY: sync
sync: $(VENV_FOLDER) ## Sync project dependencies
	@echo "$(GREEN)==> Sync project dependencies$(RESET)"
	@uv pip install -r requirements-mxdev.txt

.PHONY: install
install: $(VENV_FOLDER) config ## Install Plone and dependencies

.PHONY: clean
clean: ## Clean installation and instance
	@echo "$(RED)==> Cleaning environment and build$(RESET)"
	@rm -rf $(VENV_FOLDER) pyvenv.cfg .installed.cfg instance .venv .pytest_cache .ruff_cache constraints* requirements*

.PHONY: remove-data
remove-data: ## Remove all content
	@echo "$(RED)==> Removing all content$(RESET)"
	rm -rf $(VENV_FOLDER) instance/var

############################################
# QA
############################################
.PHONY: mypy
mypy: ## Type checking
	@echo "$(GREEN)==> Run mypy$(RESET)"
	@uv run mypy src

.PHONY: lint
lint: ## Check and fix code base according to Plone standards
	@echo "$(GREEN)==> Lint codebase$(RESET)"
	@uvx ruff@latest check --fix --config $(BACKEND_FOLDER)/pyproject.toml
	@uvx pyroma@latest -d .
	@uvx check-python-versions@latest .
	@uvx zpretty@latest --check src
	@uv run mypy src

.PHONY: format
format: ## Check and fix code base according to Plone standards
	@echo "$(GREEN)==> Format codebase$(RESET)"
	@uvx ruff@latest check --select I --fix --config $(BACKEND_FOLDER)/pyproject.toml
	@uvx ruff@latest format --config $(BACKEND_FOLDER)/pyproject.toml
	@uvx zpretty@latest -i src

.PHONY: check
check: format lint ## Check and fix code base according to Plone standards

############################################
# Tests
############################################
.PHONY: test
test: $(VENV_FOLDER) ## run tests
	@uv run pytest

.PHONY: test-coverage
test-coverage: $(VENV_FOLDER) ## run tests with coverage
	@uv run pytest -n0 --cov=pytest_plone --cov-report term-missing

############################################
# Release
############################################
.PHONY: changelog
changelog: ## Release the package to pypi.org
	@echo "🚀 Display the draft for the changelog"
	@uv run towncrier --draft

.PHONY: release
release: ## Release the package to pypi.org
	@echo "🚀 Release package"
	@uv run prerelease
	@rm -Rf dist
	@uv build
	@uv publish
	@uv run postrelease
