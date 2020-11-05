__author__ = 'tinglev'

import re
from modules.pipeline_steps.abstract_pipeline_step import AbstractPipelineStep
from modules.util import environment
from modules.util import docker
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
                    UnitTestStep.UNIT_TEST_COMPOSE_FILENAME
                ), data
            )
            self.log.debug('Output from unit tests was: %s', output)
        except Exception as ex:
             self.handle_step_error(
                    f'\n:rotating_light: <!here> {image_version_util.get_image(data)} *unit test(s) failed, see <{environment.get_build_url()}|:jenkins: Jenkins console log here>.',
                    self.get_stack_trace_shortend(ex),
                )

    def get_stack_trace_shortend(self, exception):
        error = str(exception)
        error = self.remove_possible_npm_standard_msg(error)
        error = self.remove_possible_ansibe_colors(error)

        return str(error).replace('`', ' ')[-1000:]

    def remove_possible_npm_standard_msg(self, error):
        '''
        When system exiting is not 0, npm adds crap to the output. We remove this.
        
        npm ERR! code ELIFECYCLE
        npm ERR! errno 1
        npm ERR! kth-azure-app@0.1.0 test-integration: `URL_PREFIX=http://localhost:3000/kth-azure-app ENV_TEST=SECRET_VALUE_ON__MONITOR ./tests/integration-tests/basic.sh`
        npm ERR! Exit status 1
        npm ERR!
        npm ERR! Failed at the kth-azure-app@0.1.0 test-integration script.
        npm ERR! This is
        '''
        return error[:error.find("npm ERR!")]

    def remove_possible_ansibe_colors(self, text):

        ansi_escape = re.compile(r'''
            \x1B  # ESC
            (?:   # 7-bit C1 Fe (except CSI)
                [@-Z\\-_]
            |     # or [ for CSI, followed by a control sequence
                \[
                [0-?]*  # Parameter bytes
                [ -/]*  # Intermediate bytes
                [@-~]   # Final byte
            )
            ''', re.VERBOSE)
        
        return ansi_escape.sub('', text)