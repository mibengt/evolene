__author__ = 'tinglev'

from modules.pipeline_steps.abstract_pipeline_step import AbstractPipelineStep
from modules.util.environment import Environment
from modules.util import pipeline_data

class NpmPackageNameStep(AbstractPipelineStep):

    def __init__(self):
        AbstractPipelineStep.__init__(self)

    def get_required_env_variables(self):
        return [Environment.PROJECT_ROOT]

    def get_required_data_keys(self):
        return [pipeline_data.PACKAGE_JSON]

    def run_step(self, data):
        try:
            npm_package_name = data[pipeline_data.PACKAGE_JSON]["name"]
        except KeyError as key_error:
            self.handle_step_error('Missing "name" in package.json', key_error)
        data[pipeline_data.NPM_PACKAGE_NAME] = npm_package_name
        self.log.debug('npm package name is "%s"', npm_package_name)
        return data
