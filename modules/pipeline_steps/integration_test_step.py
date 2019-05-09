__author__ = 'tinglev'

import os
from modules.pipeline_steps.abstract_pipeline_step import AbstractPipelineStep
from modules.util import environment
from modules.util import docker
from modules.util import pipeline_data
from modules.util.exceptions import PipelineException
from modules.util import file_util
from modules.util import image_version_util

class IntegrationTestStep(AbstractPipelineStep):

    INTEGRATION_TEST_COMPOSE_FILENAME = '/docker-compose-integration-tests.yml'

    def get_required_env_variables(self):
        return [environment.PROJECT_ROOT]

    def get_required_data_keys(self):
        return []

    def run_step(self, data):
        if not file_util.is_file(IntegrationTestStep.INTEGRATION_TEST_COMPOSE_FILENAME):
            self.log.info('No file named "%s" found. No integration tests will be run.', IntegrationTestStep.INTEGRATION_TEST_COMPOSE_FILENAME)
            return data

        self.run_integration_tests(data)

        return data

    def run_integration_tests(self, data):
        try:
            self.log.info(
                "Running integration tests in '%s'",
                IntegrationTestStep.INTEGRATION_TEST_COMPOSE_FILENAME
            )
            output = docker.run_integration_tests(
                file_util.get_absolue_path(
                    IntegrationTestStep.INTEGRATION_TEST_COMPOSE_FILENAME
                )
                , data
            )
            self.log.debug('Output from integration tests was: %s', output)
        except Exception as ex:
            raise PipelineException(str(ex), self.get_slack_message(ex, data))

    def get_slack_message(self, exception, data):
        return '*{}* s integration tests failed: \n```...\n{}```\n:jenkins: {}console'.format(
            image_version_util.get_image(data), 
            str(exception).replace('`', ' ')[-1000:], 
            environment.get_build_url())