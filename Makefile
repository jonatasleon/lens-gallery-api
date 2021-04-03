all: run

clean:
	rm -rf venv && rm -rf *.egg-info && rm -rf dist && rm -rf *.log*

venv:
	virtualenv --python=python3 venv && venv/bin/pip install -r requirements-dev.txt

run: venv
	venv/bin/flask run

test: venv
	venv/bin/pytest

sdist: venv test
	venv/bin/python setup.py sdist
