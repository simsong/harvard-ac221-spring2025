pylint:
	. venv/bin/activate ; pylint *py


# Create the virtual environment and install both host requirements
# and the lambda requirements for testing
venv:
	python3.12 -m venv venv
	. venv/bin/activate ; pip install --upgrade pip
	. venv/bin/activate ; if [ -r requirements.txt ] ; then pip install -r requirements.txt ; fi
	. venv/bin/activate ; if [ -r app/requirements.txt ] ; then pip install -r app/requirements.txt ; fi

.PHONY: venv
