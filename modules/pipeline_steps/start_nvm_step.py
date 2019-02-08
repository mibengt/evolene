__author__ = 'tinglev'

from modules.pipeline_steps.abstract_pipeline_step import AbstractPipelineStep
from modules.util.process import Process

class StartNvmStep(AbstractPipelineStep):

    def __init__(self):
        AbstractPipelineStep.__init__(self)

    def get_required_env_variables(self):
        return []

    def get_required_data_keys(self):
        return []

    def run_step(self, data):
        result = Process.run_with_output('. /var/lib/jenkins/.nvm/nvm.sh && nvm --version')
        self.log.debug('nvm version is: "%s"', result.strip())
        return data
