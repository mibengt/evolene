#!/bin/sh
WORKSPACE=./test/data pipenv run green -vv --run-coverage --failfast "test"