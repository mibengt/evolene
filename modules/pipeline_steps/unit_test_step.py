__author__ = 'tinglev'

import os
from modules.pipeline_steps.abstract_pipeline_step import AbstractPipelineStep
from modules.util.environment import Environment
from modules.util.docker import Docker
from modules.util.data import Data
from modules.util.exceptions import PipelineException

class UnitTestStep(AbstractPipelineStep):

    def get_required_env_variables(self):
        return [Environment.PROJECT_ROOT]

    def get_required_data_keys(self):
        return []

    def run_step(self, data):
        
        compose_test_file = self.get_absolut_test_file_path()
        if self.test_file_exists(compose_test_file):
            self.log.info('Running unit tests.')
            self.run_unit_tests(compose_test_file, data)
        else:
            self.log.info('No file named "%s" found. No unit tests will be run.',
                          compose_test_file)
        return data

    def get_absolut_test_file_path(self):
        stripped_root = Environment.get_project_root().rstrip('/')
        return '{}/{}'.format(stripped_root, Docker.UNIT_TEST_COMPOSE_FILENAME)

    def test_file_exists(self, compose_test_file):
        return os.path.exists(compose_test_file)

    def run_unit_tests(self, compose_test_file, data):
        try:
            Docker.run_unit_test_compose(compose_test_file, data)
        except Exception as ex:
            raise PipelineException('*{}* Unit tests failed: \n{}\n\n:jenkins: {}console'
                                    .format(data[Data.IMAGE_NAME], ex.message.replace('`', ' '), Environment.get_build_url()))
