__author__ = 'tinglev'

from modules.pipeline_steps.abstract_pipeline_step import AbstractPipelineStep
from modules.util.environment import Environment
from modules.util.data import Data

class NpmVersionStep(AbstractPipelineStep):

    def __init__(self):
        AbstractPipelineStep.__init__(self)

    def get_required_env_variables(self):
        return [Environment.PROJECT_ROOT]

    def get_required_data_keys(self):
        return [Data.PACKAGE_JSON]

    def run_step(self, data):
        npm_version = data[Data.PACKAGE_JSON]["version"]
        data[Data.NPM_VERSION] = npm_version
        self.log.debug('npm version of application is "%s"', npm_version)
        return data
