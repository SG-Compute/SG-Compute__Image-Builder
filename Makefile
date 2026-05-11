.PHONY: help install lint format typecheck test unit integration e2e zipapp clean

PYTHON ?= python

help:
	@echo 'sgi - common dev targets'
	@echo
	@echo '  make install      Install package + test deps (editable)'
	@echo '  make lint         Run ruff check + ruff format --check'
	@echo '  make format       Apply ruff format'
	@echo '  make typecheck    Run mypy on sg_image_builder/'
	@echo '  make test         Run unit + integration tests'
	@echo '  make unit         Run unit tests only'
	@echo '  make integration  Run integration tests only'
	@echo '  make e2e          Run end-to-end tests (requires SGI_E2E_ENABLED=1)'
	@echo '  make zipapp       Build dist/sgi.zipapp'
	@echo '  make clean        Remove build / cache artefacts'

install:
	$(PYTHON) -m pip install -e .[test,dev]

lint:
	$(PYTHON) -m ruff check sg_image_builder/ sg_image_builder__tests/
	$(PYTHON) -m ruff format --check sg_image_builder/ sg_image_builder__tests/

format:
	$(PYTHON) -m ruff format sg_image_builder/ sg_image_builder__tests/

typecheck:
	$(PYTHON) -m mypy sg_image_builder/

test: unit integration

unit:
	$(PYTHON) -m pytest sg_image_builder__tests/unit/ -v

integration:
	$(PYTHON) -m pytest sg_image_builder__tests/integration/ -v

e2e:
	SGI_E2E_ENABLED=1 $(PYTHON) -m pytest sg_image_builder__tests/end_to_end/ -v

zipapp:
	$(PYTHON) scripts/build_zipapp.py

clean:
	rm -rf dist/ build/ .pytest_cache/ .mypy_cache/ .ruff_cache/ .coverage
	find . -name __pycache__ -type d -prune -exec rm -rf {} +
	find . -name '*.egg-info' -type d -prune -exec rm -rf {} +
