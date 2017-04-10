__author__ = 'tinglev'

import os

class Environment(object):

    IMAGE_NAME = 'IMAGE_NAME'
    IMAGE_VERSION = 'IMAGE_VERSION'
    PROJECT_ROOT = 'PROJECT_ROOT_PATH'
    GIT_COMMIT = 'GIT_COMMIT'
    BUILD_NUMBER = 'BUILD_NUMBER'
    SLACK_WEB_HOOK = 'SLACK_WEB_HOOK'
    SLACK_CHANNELS = 'SLACK_CHANNELS'
    REGISTRY_HOST = 'REGISTRY_HOST'

    @staticmethod
    def get_registry_host():
        return os.environ[Environment.REGISTRY_HOST]

    @staticmethod
    def get_image_name():
        return os.environ[Environment.IMAGE_NAME]

    @staticmethod
    def get_image_version():
        return os.environ[Environment.IMAGE_VERSION]

    @staticmethod
    def get_git_commit():
        return os.environ[Environment.GIT_COMMIT]

    @staticmethod
    def get_project_root():
        return os.environ[Environment.PROJECT_ROOT]

    @staticmethod
    def get_build_number():
        return os.environ[Environment.BUILD_NUMBER]
