VENV=./venv
PYTHON=$(VENV)/bin/python3

venv:
	python3 -m venv $(VENV)

setup:
	pip install -r ai/ai_requirements.txt
