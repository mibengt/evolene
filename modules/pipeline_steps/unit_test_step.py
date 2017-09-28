__author__ = 'tinglev'

import os
from modules.pipeline_steps.abstract_pipeline_step import AbstractPipelineStep
from modules.util.environment import Environment
from modules.util.docker import Docker
from modules.util.exceptions import PipelineException

class UnitTestStep(AbstractPipelineStep):

    def get_required_env_variables(self):
        return [Environment.PROJECT_ROOT]

    def get_required_data_keys(self):
        return []

    def run_step(self, data):
        compose_test_file = Docker.UNIT_TEST_COMPOSE_FILENAME
        if self.test_file_exists():
            self.run_unit_tests()
        else:
            self.log.info('No file named "%s" found. No unit tests will be run.',
                          compose_test_file)
        return data

    def test_file_exists(self):
        return os.path.exists(Docker.UNIT_TEST_COMPOSE_FILENAME)

    def run_unit_tests(self):
        try:
            Docker.run_unit_test_compose()
        except Exception as ex:
            raise PipelineException('Unit tests failed with message: {}'
                                    .format(ex.message))
