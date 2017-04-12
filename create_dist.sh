#!/bin/sh

virtualenv env
env/bin/pip install -r requirements.txt
./run_tests.sh
env/bin/python setup.py sdist