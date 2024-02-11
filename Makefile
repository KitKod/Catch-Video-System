# Makefile

# Project variables
VENV_NAME ?= venv
PYTHON := $(VENV_NAME)/bin/python
PIP := $(VENV_NAME)/bin/pip

# Default command to run when no target is specified
all: run

# Create virtual environment
venv: $(VENV_NAME)/bin/activate
$(VENV_NAME)/bin/activate: requirements.txt
	test -d $(VENV_NAME) || python3 -m venv $(VENV_NAME)
	${PIP} install -U pip
	${PIP} install -r requirements.txt
	touch $(VENV_NAME)/bin/activate

# Reinstall dependencies from requirements.txt
reinstall-dependencies: $(VENV_NAME)/bin/activate
	${PIP} install --force-reinstall -r requirements.txt

# Run your application
client: venv
	$(PYTHON) client.py

server: venv
	$(PYTHON) app.py

stop:
	@echo "Stopping application..." # Implement actual stop command

# Clean up the project
clean:
	rm -rf $(VENV_NAME)
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -exec rm -rf {} +

help:
	@echo "Makefile for managing the Python project"
	@echo ""
	@echo "Commands:"
	@echo "venv                   Create a virtual environment and install dependencies"
	@echo "reinstall-dependencies Reinstall all dependencies from requirements.txt"
	@echo "client                 Run the client application"
	@echo "server                 Run the server application"
	@echo "stop                   Stop the application (modify as needed)"
	@echo "clean                  Remove the virtual environment and cleanup files"
