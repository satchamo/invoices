# run tests for python 3
test: .env
	.env/bin/python runtests.py && .env/bin/flake8 && .env/bin/isort -rc --diff --check-only invoices

# remove junk
clean:
	rm -rf .env *.pyc

# setup a virtualenv for python3 and install pip
.env:
	python3 -m venv --without-pip .env
	curl https://raw.githubusercontent.com/pypa/pip/master/contrib/get-pip.py | .env/bin/python
	.env/bin/pip install -e .[test]
