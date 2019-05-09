__author__ = 'tinglev'

from modules.pipeline_steps.abstract_pipeline_step import AbstractPipelineStep
from modules.util import environment
from modules.util import docker
from modules.util import pipeline_data
from modules.util.exceptions import PipelineException
from modules.util import file_util
from modules.util import image_version_util


class UnitTestStep(AbstractPipelineStep):

    UNIT_TEST_COMPOSE_FILENAME = '/docker-compose-unit-tests.yml'

    def get_required_env_variables(self):
        return [environment.PROJECT_ROOT]

    def get_required_data_keys(self):
        return []

    def run_step(self, data):

        if not file_util.is_file(UnitTestStep.UNIT_TEST_COMPOSE_FILENAME):
            self.log.info('No file named "%s" found. No unit tests will be run.',
                          UnitTestStep.UNIT_TEST_COMPOSE_FILENAME)
            return data

        self.run_unit_tests(data)

        return data

    def run_unit_tests(self, data):
        try:
            output = docker.run_unit_test_compose(
                file_util.get_absolue_path(
                    UnitTestStep.UNIT_TEST_COMPOSE_FILENAME)
                    , data
                )
            self.log.debug('Output from unit tests was: %s', output)
        except Exception as ex:
            raise PipelineException(
                str(ex), self.get_slack_message(ex, data))

    def get_slack_message(self, exception, data):
        return '*{}* Unit test(s) failed: \n```...\n{}```\n:jenkins: {}console'.format(
            image_version_util.get_image(data),
            str(exception).replace('`', ' ')[-1000:],
            environment.get_build_url())
