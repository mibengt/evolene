__author__ = 'tinglev'

import os
from modules.pipeline_steps.abstract_pipeline_step import AbstractPipelineStep
from modules.util.environment import Environment
from modules.util.docker import Docker
from modules.util.data import Data
from modules.util.exceptions import PipelineException

class IntegrationTestStep(AbstractPipelineStep):

    def get_required_env_variables(self):
        return [Environment.PROJECT_ROOT]

    def get_required_data_keys(self):
        return []

    def run_step(self, data):
        compose_test_file = self.get_absolut_test_file_path()
        if self.test_file_exists(compose_test_file):
            self.log.info('Running integration tests.')
            self.run_integration_tests(compose_test_file, data)
        else:
            self.log.info('No file named "%s" found. No integration tests will be run.',
                          compose_test_file)
        return data

    def get_absolut_test_file_path(self):
        stripped_root = Environment.get_project_root().rstrip('/')
        return '{}/{}'.format(stripped_root, Docker.INTEGRATION_TEST_COMPOSE_FILENAME)

    def test_file_exists(self, compose_test_file):
        return os.path.exists(compose_test_file)

    def run_integration_tests(self, compose_test_file, data):
        try:
            Docker.run_integration_tests(compose_test_file, data)
        except Exception as ex:
            raise PipelineException(ex.message, self.get_slack_message(ex, data))

    def get_slack_message(self, exception, data):
        return '*{}* s integration tests failed: \n```...\n{}```\n:jenkins: {}console'.format(
            data[Data.IMAGE_NAME], 
            exception.message.replace('`', ' ')[-1000:], 
            Environment.get_build_url())