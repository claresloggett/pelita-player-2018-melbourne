# Throws a coin. Sets RAND to 0 or 1.
RAND := $(shell awk 'BEGIN{srand();printf("%d", 2*rand())}')

# Our default factory method
FACTORY = team/

PELITA_OPTIONS =

.PHONY: default run test

default: run

run:
	@echo "Running a quick match against a default player"
ifeq ($(RAND), 0)
	@$(MAKE) left
else
	@$(MAKE) right
endif

left:
	pelita $(FACTORY) random $(PELITA_OPTIONS)

right:
	pelita random $(FACTORY) $(PELITA_OPTIONS)

test:
	@echo "Running the test suite"
	PYTHONPATH=. py.test test/
