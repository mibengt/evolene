__author__ = 'tinglev'

import os
import datetime
import time

class Environment(object):

    IMAGE_NAME = 'IMAGE_NAME'
    PROJECT_ROOT = 'WORKSPACE'
    GIT_COMMIT = 'GIT_COMMIT'
    GIT_BRANCH = 'GIT_BRANCH'
    GIT_COMMITTER_NAME = 'GIT_COMMITTER_NAME'
    BUILD_NUMBER = 'BUILD_NUMBER'
    BUILD_URL = 'BUILD_URL'
    BUILD_INFORMATION_OUTPUT_FILE = 'BUILD_INFORMATION_OUTPUT_FILE'
    SLACK_WEB_HOOK = 'EVOLENE_SLACK_WEB_HOOK'
    SLACK_CHANNELS = 'SLACK_CHANNELS'
    REGISTRY_HOST = 'REGISTRY_HOST'
    REGISTRY_USER = 'REGISTRY_USER'
    REGISTRY_PASSWORD = 'REGISTRY_PASSWORD'
    EVOLENE_DIRECTORY = 'EVOLENE_DIRECTORY'
    EXPERIMENTAL = 'EXPERIMENTAL'
    SKIP_DRY_RUN = 'SKIP_DRY_RUN'
    PUSH_PUBLIC = 'PUSH_PUBLIC'
    PUSH_AZURE = 'PUSH_AZURE'
    AZURE_REGISTRY_HOST = 'AZURE_REGISTRY_HOST'
    AZURE_REGISTRY_USER = 'AZURE_REGISTRY_USER'
    AZURE_REGISTRY_PASSWORD = 'AZURE_REGISTRY_PASSWORD'

    @staticmethod
    def get_registry_host():
        if Environment.get_push_public():
            return "docker.io/kthse"
        if Environment.get_push_azure():
            return os.environ.get(Environment.AZURE_REGISTRY_HOST)
        return os.environ.get(Environment.REGISTRY_HOST)

    @staticmethod
    def get_registry_user():
        if Environment.get_push_azure():
            return os.environ.get(Environment.AZURE_REGISTRY_USER)
        return os.environ.get(Environment.REGISTRY_USER)

    @staticmethod
    def get_registry_password():
        if Environment.get_push_azure():
            return os.environ.get(Environment.AZURE_REGISTRY_PASSWORD)
        return os.environ.get(Environment.REGISTRY_PASSWORD)

    @staticmethod
    def get_image_name():
        return os.environ.get(Environment.IMAGE_NAME)

    @staticmethod
    def get_git_commit():
        return os.environ.get(Environment.GIT_COMMIT)

    @staticmethod
    def get_git_branch():
        return os.environ.get(Environment.GIT_BRANCH)

    @staticmethod
    def get_git_commiter_name():
        return os.environ.get(Environment.GIT_COMMITTER_NAME)

    @staticmethod
    def get_project_root():
        return os.environ.get(Environment.PROJECT_ROOT)

    @staticmethod
    def get_build_number():
        return os.environ.get(Environment.BUILD_NUMBER)

    @staticmethod
    def get_build_information_output_file():
        return os.environ.get(Environment.BUILD_INFORMATION_OUTPUT_FILE)

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

    @staticmethod
    def get_push_public():
        return Environment.is_true(Environment.PUSH_PUBLIC)

    @staticmethod
    def get_push_azure():
        return Environment.is_true(Environment.PUSH_AZURE)

    @staticmethod
    def get_experimental():
        return Environment.is_true(Environment.EXPERIMENTAL)

    @staticmethod
    def use_dry_run():
        if Environment.is_true(Environment.SKIP_DRY_RUN):
            return False
        return True

    @staticmethod
    def get_build_url():
        return os.environ.get(Environment.BUILD_URL)

    @staticmethod
    def is_true(env_key):
        value = os.environ.get(env_key)
        if value is None:
            return False

        return value.lower() in ['true', 'yes', 'y']

    @staticmethod
    def get_time():
        return datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
