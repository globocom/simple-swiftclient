.PHONY: clean setup run pep8 tests

CWD="`pwd`"
PROJECT_NAME = simple-swiftclient
PROJECT_HOME ?= $(CWD)

clean:
	@echo "Cleaning up *.pyc files"
	@find . -name "*.pyc" -delete
	@find . -name "*.~" -delete

pep8:
	@echo "Checking source-code PEP8 compliance"
	@-pep8 $(PROJECT_HOME) --ignore=E501,E126,E127,E128

tests: clean pep8
	@echo "Running pep8 and all tests with coverage"
	@py.test --cov-config .coveragerc --cov $(PROJECT_HOME) --cov-report term-missing
