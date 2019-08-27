__author__ = 'tinglev'

from modules.pipeline_steps.abstract_pipeline_step import AbstractPipelineStep
from modules.util import pipeline_data, slack, nvm, environment

class NpmPublishStep(AbstractPipelineStep):

    def __init__(self):
        AbstractPipelineStep.__init__(self)

    def get_required_env_variables(self):
        return []

    def get_required_data_keys(self):
        return [pipeline_data.NPM_VERSION_CHANGED, pipeline_data.NPM_PACKAGE_VERSION,
                pipeline_data.NPM_LATEST_VERSION, pipeline_data.NPM_PACKAGE_NAME]

    def run_step(self, data):
        if data[pipeline_data.NPM_VERSION_CHANGED]:
            self.log.info(
                'Package will be published. Local version is %s and '
                'latest version on npm is %s',
                data[pipeline_data.NPM_PACKAGE_VERSION],
                data[pipeline_data.NPM_LATEST_VERSION]
            )
            flags = environment.get_project_root()
            result = nvm.exec_npm_command(data, 'publish', flags)
            self.log.debug('Result from npm publish was: "%s"', result)
            slack.on_npm_publish(data[pipeline_data.NPM_PACKAGE_NAME],
                                 data[pipeline_data.NPM_PACKAGE_VERSION],
                                 data)
        else:
            self.log.debug('Version hasnt changed, skipping publish')
            slack.on_npm_no_publish(data[pipeline_data.NPM_PACKAGE_NAME],
                                 data[pipeline_data.NPM_PACKAGE_VERSION])
        return data
