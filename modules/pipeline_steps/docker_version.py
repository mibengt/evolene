__author__ = 'paddy'

from modules.pipeline_steps.abstract_pipeline_step import AbstractPipelineStep
from modules.util.exceptions import PipelineException
from modules.util import process
from modules.util import print_util

class DockerVersion(AbstractPipelineStep):

    def __init__(self):
        AbstractPipelineStep.__init__(self)

    def get_required_env_variables(self):
        return []

    def get_required_data_keys(self):
        return []

    def run_step(self, data):
        try:
            print_util.green(process.run_with_output('docker --version'))
            
        except PipelineException as install_ex:
            self.handle_step_error('Error while checking Docker version. ', install_ex)
