__author__ = 'tinglev'

from modules.pipeline_steps.abstract_pipeline_step import AbstractPipelineStep
from modules.util.environment import Environment
from modules.util.exceptions import PipelineException
from modules.util import nvm, pipeline_data

class NpmVersionChangedStep(AbstractPipelineStep):

    def __init__(self):
        AbstractPipelineStep.__init__(self)

    def get_required_env_variables(self):
        return [Environment.PROJECT_ROOT]

    def get_required_data_keys(self):
        return [pipeline_data.NPM_PACKAGE_VERSION, pipeline_data.NPM_PACKAGE_NAME]

    def run_step(self, data):
        current_version = data[pipeline_data.NPM_PACKAGE_VERSION]
        package_name = data[pipeline_data.NPM_PACKAGE_NAME]
        result = self.get_latest_version(package_name, data)
        self.log.debug('Latest version published is: "%s"', result)
        data[pipeline_data.NPM_LATEST_VERSION] = result
        data[pipeline_data.NPM_VERSION_CHANGED] = (current_version != result)
        self.log.debug('npm version has changed "%s"', data[pipeline_data.NPM_VERSION_CHANGED])
        return data

    def get_latest_version(self, package_name, data):
        try:
            return nvm.exec_npm_command(data, f'show {package_name} version')
        except PipelineException as npm_ex:
            self.handle_step_error(
                'Exception when getting published npm version for package',
                npm_ex
            )
