__author__ = 'tinglev'

import os

class Environment(object):

    IMAGE_NAME = 'IMAGE_NAME'
    PROJECT_ROOT = 'PROJECT_ROOT_PATH'
    GIT_COMMIT = 'GIT_COMMIT'
    BUILD_NUMBER = 'BUILD_NUMBER'
    SLACK_WEB_HOOK = 'SLACK_WEB_HOOK'
    SLACK_CHANNELS = 'SLACK_CHANNELS'
    REGISTRY_HOST = 'REGISTRY_HOST'
    REGISTRY_USER = 'REGISTRY_USER'
    REGISTRY_PASSWORD = 'REGISTRY_PASSWORD'
    EVOLENE_DIRECTORY = 'EVOLENE_DIRECTORY'

    @staticmethod
    def get_registry_host():
        return os.environ.get(Environment.REGISTRY_HOST)

    @staticmethod
    def get_registry_user():
        return os.environ.get(Environment.REGISTRY_USER)

    @staticmethod
    def get_registry_password():
        return os.environ.get(Environment.REGISTRY_PASSWORD)

    @staticmethod
    def get_image_name():
        return os.environ.get(Environment.IMAGE_NAME)

    @staticmethod
    def get_git_commit():
        return os.environ.get(Environment.GIT_COMMIT)

    @staticmethod
    def get_project_root():
        return os.environ.get(Environment.PROJECT_ROOT)

    @staticmethod
    def get_build_number():
        return os.environ.get(Environment.BUILD_NUMBER)

    @staticmethod
    def get_slack_channels():
        channels = os.environ.get(Environment.SLACK_CHANNELS)
        return [channel.rstrip() for channel in channels.split(',')]

    @staticmethod
    def get_slack_web_hook():
        return os.environ.get(Environment.SLACK_WEB_HOOK)

    @staticmethod
    def get_evolene_directory():
        return os.environ.get(Environment.EVOLENE_DIRECTORY)
