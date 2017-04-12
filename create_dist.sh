#!/bin/sh

virtualenv env
env/bin/pip install -r requirements.txt
python setup.py sdist