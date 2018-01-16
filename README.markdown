# Pelita demo player module

## Notes on writing

* Please use Python 3
* Numpy is pre-installed on the tournament machine; everything else must be negotiated
* Please use relative imports inside your module
* You may need to set the PYTHONPATH to point to the main pelita directory for the tests or simply run `make test` from the repository

## Files

### team/

The main module which contains all your team’s code. Please use relative imports from inside the module.

### team/__init__.py

Builds the final teams and exports the factory methods. When using the module on the command line, such as in

    pelita path/to/module/team

the method defined with `def team` is automatically called. Different methods can be specified with a colon

    pelita path/to/module/team:other_team

### team/demo_player.py

Contains the code for a simple demo player.

### team/utils.py

This could be a good place for global utility functions (but feel free to add more files for this, if needed)

### test/test_demo_player.py

Simple unittest for your player. Note the relative imports. You can run tests using py.test, which automatically executes all tests in the `test/` directory.

    $ py.test test/
    .
    ----------------------------------------------------------------------
    Ran 1 test in 0.025s

    OK


## Makefile

We have a `Makefile` for a few quick tasks.

Per default, running `make` will start a game against a random player, and randomly choosing the side, the team is playing at. Running an explicit `make left` or `make right` will specify the position. (For more control, it is of course advised to use the `pelita` command directly.

`make test` will run `pytest` on the `test/` directory, so be sure to run it once in a while. And also add your own tests to the test folder.
