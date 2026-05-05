PYTHON := python
VENV_DIR := .venv

ifeq ($(OS),Windows_NT)
VENV_PYTHON := $(VENV_DIR)/Scripts/python.exe
else
VENV_PYTHON := $(VENV_DIR)/bin/python
endif

.PHONY: install run test uninstall

install:
	$(PYTHON) -m venv $(VENV_DIR)
	$(VENV_PYTHON) -m pip install --upgrade pip
	$(VENV_PYTHON) -m pip install -e .[dev]

run:
	$(VENV_PYTHON) src/main.py --length 16

test:
	$(VENV_PYTHON) -m pytest -q

uninstall:
	$(VENV_PYTHON) -m pip uninstall -y password-generator
