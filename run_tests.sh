#!/bin/sh
PIPENV_VERBOSITY=-1 WORKSPACE=./test/data pipenv run green -vv --run-coverage --failfast "test"
#PIPENV_VERBOSITY=-1 WORKSPACE=./test/data pipenv run green --failfast "test"