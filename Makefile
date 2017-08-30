

.PHONY: default run test

default: run

run:
	@echo "Running a quick match against a default player"
	pelita team/

test:
	@echo "Running the test suite"
	PYTHONPATH=. py.test test/


