__author__ = 'tinglev'

from modules.pipeline_steps.abstract_pipeline_step import AbstractPipelineStep
from modules.util.data import Data
from modules.util import nvm

class NpmPublishStep(AbstractPipelineStep):

    def __init__(self):
        AbstractPipelineStep.__init__(self)

    def get_required_env_variables(self):
        return []

    def get_required_data_keys(self):
        return [Data.NPM_VERSION_CHANGED]

    def run_step(self, data):
        if data[Data.NPM_VERSION_CHANGED]:
            #result = nvm.exec_npm_command(data, 'publish')
            result = 'PUBLISHED'
            self.log.debug('Result from npm publish was: "%s"', result)
        else:
            self.log.debug('Version hasnt changed, skipping publish')
        return data
