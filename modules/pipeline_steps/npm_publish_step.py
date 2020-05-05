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

    def should_auto_update(self, data):
        '''
        If version only is "major.minor" then Evolene should add the last patch version.
        '''
        version = data[pipeline_data.NPM_PACKAGE_VERSION]
        if version.count('.') == 1:
            return True
        return False

    def get_patch_version_from_npm_latest_version(self, data):
        version = data[pipeline_data.NPM_LATEST_VERSION]
        self.log.info('Last published version on MPM: %s', version)
        patch_version = version.find(".", version.find("."))
        return patch_version

    def get_auto_update_version(self, data):
        majorMinorVersion = data[pipeline_data.PACKAGE_JSON]["majorMinorVersion"]
        updated_patch_version = self.get_patch_version_from_npm_latest_version(data) + 1
        version = f"{majorMinorVersion}.{updated_patch_version}"
        data[pipeline_data.NPM_PACKAGE_VERSION] = version
        return version

    def write_auto_updated_package_json(self, data):
        data[pipeline_data.PACKAGE_JSON]["version"] = self.get_auto_update_version(data)
        file_util.overwite('/package.npm.json', json.dumps(data[pipeline_data.PACKAGE_JSON]))
        data[pipeline_data.NPM_VERSION_CHANGED] = True 
       
    def run_step(self, data):
        if self.should_auto_update(data):
            self.write_auto_updated_package_json(data)

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
