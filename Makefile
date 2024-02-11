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

# Run your application
run: venv
	$(PYTHON) your_application.py

# Example command to run your application in a different way
# For instance, starting a web server, etc.
serve: venv
	$(PYTHON) your_server.py

# Stop application (Modify as needed; this is just a placeholder)
stop:
	@echo "Stopping application..." # Implement actual stop command

# Clean up the project
clean:
	rm -rf $(VENV_NAME)
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -exec rm -rf {} +

# Help
help:
	@echo "Makefile for managing the Python project"
	@echo ""
	@echo "Commands:"
	@echo "venv    Create a virtual environment and install dependencies"
	@echo "run     Run the application"
	@echo "serve   Serve the application (if applicable)"
	@echo "stop    Stop the application (modify as needed)"
	@echo "clean   Remove the virtual environment and cleanup files"
