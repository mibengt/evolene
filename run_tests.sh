#!/bin/sh

RUN_WITH_VIRTUALENV=TRUE

virtualenv -v .tmp >/dev/null 2>&1 || {
  echo "No virtualenv installed."
  rm -rf .tmp
  exit 1
}
rm -rf .tmp

echo "Virtualenv environment 'env' used for tests."
virtualenv env
env/bin/pip install -r requirements.txt
env/bin/green "test" -vv --run-coverage