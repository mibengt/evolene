__author__ = 'tinglev'

from modules.pipeline_steps.abstract_pipeline_step import AbstractPipelineStep
from modules.util.environment import Environment
from modules.util.data import Data
from modules.util import nvm

class NpmTestStep(AbstractPipelineStep):

    def __init__(self):
        AbstractPipelineStep.__init__(self)

    def get_required_env_variables(self):
        return [Environment.PROJECT_ROOT]

    def get_required_data_keys(self):
        return [Data.NPM_CONF_NODE_VERSION]

    def run_step(self, data):
        result = nvm.run_npm_script(data, 'test')
        self.log.debug('Output from npm test was: "%s"', result)
        return data
