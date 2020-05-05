__author__ = 'tinglev'

import json
from modules.pipeline_steps.abstract_pipeline_step import AbstractPipelineStep
from modules.util import pipeline_data, slack, nvm, environment
from modules.util import file_util

class NpmPublishStep(AbstractPipelineStep):

    def __init__(self):
        AbstractPipelineStep.__init__(self)

    def get_required_env_variables(self):
        return []

    def get_required_data_keys(self):
        return [pipeline_data.NPM_VERSION_CHANGED, pipeline_data.NPM_PACKAGE_VERSION,
                pipeline_data.NPM_LATEST_VERSION, pipeline_data.NPM_PACKAGE_NAME]


    def get_next_version(self, data):
        self.log.info('Package.json / version: %s', data[pipeline_data.NPM_PACKAGE_VERSION])
        package_json = data[pipeline_data.PACKAGE_JSON]
        package_json["version"] = "0.0.0"
        file_util.overwite('/package.new.json', json.dumps(package_json))
       
    def run_step(self, data):
        self.get_next_version(data)

        # Skip publish on pull request testing
        if environment.get_pull_request_test():
            return data
        if data[pipeline_data.NPM_VERSION_CHANGED]:
            self.log.info(
                'Package will be published. Local version is %s and '
                'latest version on npm is %s',
                data[pipeline_data.NPM_PACKAGE_VERSION],
                data[pipeline_data.NPM_LATEST_VERSION]
            )
            flags = environment.get_project_root()
            result = nvm.exec_npm_command(data, 'publish --access public', flags)
            self.log.debug('Result from npm publish was: "%s"', result)
            slack.on_npm_publish(data[pipeline_data.NPM_PACKAGE_NAME],
                                 data[pipeline_data.NPM_PACKAGE_VERSION],
                                 data)
        else:
            self.log.debug('Version hasnt changed, skipping publish')
            slack.on_npm_no_publish(data[pipeline_data.NPM_PACKAGE_NAME],
                                    data[pipeline_data.NPM_PACKAGE_VERSION])
        return data
