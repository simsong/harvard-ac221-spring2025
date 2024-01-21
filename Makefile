#
# Note: when this runs on Dreamhost, we need to use the python in $HOME/opt/bin
#

PYLINT_FILES=$(shell /bin/ls *.py)
PYTHON=python3.11
PIP_INSTALL=$(PYTHON) -m pip install --no-warn-script-location --user

# By default, PYLINT generates an error if your code does not rank 10.0.
# This makes us tolerant of minor problems.
PYLINT_THRESHOLD=9.5

all:
	@echo verify syntax and then restart
	make pylint
	make touch

check:
	make pylint
	make pytest

touch:
	touch tmp/restart.txt

pylint:
	pylint --rcfile .pylintrc --fail-under=$(PYLINT_THRESHOLD) --verbose $(PYLINT_FILES)

flake8:
	flake8 $(PYLINT_FILES)

pytest:
	$(PYTHON) -m pytest --log-cli-level=DEBUG .

coverage:
	$(PYTHON) -m pip install --upgrade pip
	$(PIP_INSTALL) codecov pytest pytest_cov
	$(PYTHON) -m pytest -v --cov=. --cov-report=xml tests

clean:
	find . -name '*~' -exec rm {} \;


################################################################
# Installations are used by the CI pipeline:
# Generic:
install-python-dependencies:
	$(PYTHON) -m pip install --upgrade pip
	if [ -r requirements.txt ]; then $(PIP_INSTALL) -r requirements.txt ; else echo no requirements.txt ; fi

install-ubuntu:
	make install-python-dependencies

# Includes MacOS dependencies managed through Brew
install-macos:
	brew update
	brew upgrade
	brew install python3
	make install-python-dependencies
	if [ -r requirements-macos.txt ]; then $(PIP_INSTALL) -r requirements-macos.txt ; else echo no requirements-ubuntu.txt ; fi


# Includes Windows dependencies
install-windows:
	make install-python-dependencies
	if [ -r requirements-windows.txt ]; then $(PIP_INSTALL) -r requirements-windows.txt ; else echo no requirements-ubuntu.txt ; fi
