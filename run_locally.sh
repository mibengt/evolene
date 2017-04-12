#!/bin/sh

DEBUG=True \
GIT_COMMIT=abc1237XXXXX \
BUILD_NUMBER=123 \
PROJECT_ROOT_PATH=/Users/tinglev/Repos/evolene/test/data \
IMAGE_NAME=evolene \
REGISTRY_HOST=kthregistryv2.sys.kth.se \
REGISTRY_USER=jenkins \
SLACK_CHANNELS=#pipeline-logs \
SLACK_WEB_HOOK=not_at_this_time \
env/bin/python run.py docker run-pipeline