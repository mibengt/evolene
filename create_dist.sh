#!/bin/sh

set -e

pipenv install
./run_tests.sh
pipenv run python setup.py sdist