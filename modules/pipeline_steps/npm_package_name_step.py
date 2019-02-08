__author__ = 'tinglev'

from modules.pipeline_steps.abstract_pipeline_step import AbstractPipelineStep
from modules.util.environment import Environment
from modules.util.data import Data

class NpmPackageNameStep(AbstractPipelineStep):

    def __init__(self):
        AbstractPipelineStep.__init__(self)

    def get_required_env_variables(self):
        return [Environment.PROJECT_ROOT]

    def get_required_data_keys(self):
        return [Data.PACKAGE_JSON]

    def run_step(self, data):
        try:
            npm_package_name = data[Data.PACKAGE_JSON]["name"]
        except KeyError as key_error:
            self.handle_step_error('Missing "name" in package.json', key_error)
        data[Data.NPM_PACKAGE_NAME] = npm_package_name
        self.log.debug('npm package name is "%s"', npm_package_name)
        return data
