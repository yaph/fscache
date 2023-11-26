.PHONY: clean clean-test clean-pyc clean-build help

clean: clean-build clean-pyc clean-test ## remove all build, test, coverage and Python artifacts

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	rm -fr .fscache/*
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr .pytest_cache

lint: ## check style with flake8
	flake8 fscache tests

test: ## run tests quickly with the default Python
	py.test

typecheck:
	mypy --ignore-missing-imports fscache

coverage: ## check code coverage quickly with the default Python
	coverage run --source fscache -m pytest
	coverage report -m

dist: clean ## builds source and wheel package
	python setup.py sdist
	python setup.py bdist_wheel
	ls -l dist

install: clean ## install the package to the active Python's site-packages
	python setup.py install

install-test:
	pip install -r requirements_test.txt

install-all: install install-test
	pip install -r requirements_dev.txt

# Package and upload a release. Call example: make release version=0.3.0
release: dist
	git tag -a $(version) -m 'Create version $(version)'
	git push --tags
	twine upload dist/*