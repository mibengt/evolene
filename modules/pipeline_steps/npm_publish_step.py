__author__ = 'tinglev'

import json
import os
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

    def use_automatic_publish(self, data):
        try:
            automatic_publish = data[pipeline_data.PACKAGE_JSON]["automaticPublish"]
        except:
            return False

        if environment.is_true_value(automatic_publish):
            self.log.info('Will automatic puublish with increased patch version in package.json')
            return True
        
        self.log.info('No automatic publish, using version in package.json')
        return False

    def get_latest_patch_version(self, data):
        '''
        From "2.3.45"  latest published npm version
        return "45" to use as major.minor when se.kth.automaticPublish is true
        '''
        version = data[pipeline_data.NPM_LATEST_VERSION]
        # Read the last didgit = "1.2.[3]"
        patch_version_index = version.rfind(".") + 1
        patch_version = version[patch_version_index:]
        self.log.debug('Next free patch version is: %s', patch_version)
        return int(patch_version)

    def get_next_patch_version(self, data):
        return self.get_latest_patch_version(data) + 1

    def get_major_minor_version(self, data):
        '''
        From "2.3.45"  latest published npm version
        return "2.3" to use as major.minor when se.kth.automaticPublish is true
        '''
        version = data[pipeline_data.NPM_LATEST_VERSION]
        # Read the last didgit = "1.2.[3]"
        major_minor_index = version.rfind(".")
        major_minor_version = version[:major_minor_index]
        self.log.debug('Major minor version is: %s', major_minor_version)
        return major_minor_version

    def get_next_version(self, data):
        major_minor_version = self.get_major_minor_version(data)
        next_patch_version = self.get_next_patch_version(data)
        next_version = f"{major_minor_version}.{next_patch_version}"
        self.log.info('Auto update resulted in npm publish using %s as version', next_version)
        data[pipeline_data.NPM_PACKAGE_VERSION] = next_version
        return next_version

    def update_patch_version(self, data):
        data[pipeline_data.PACKAGE_JSON]["version"] = self.get_next_version(data)
        data[pipeline_data.PACKAGE_JSON]["se.kth.automaticPublish"] = "true"
        data[pipeline_data.NPM_VERSION_CHANGED] = True

    def write_updated_package_json(self, data):
        file_util.overwite('/package.json', json.dumps(data[pipeline_data.PACKAGE_JSON]))
        self.log.info('Wrote updated package.json to disc, ready for npm publish.')

    def run_step(self, data):
        if self.use_automatic_publish(data):
            self.update_patch_version(data)

        data[pipeline_data.PACKAGE_JSON]["se.kth.gitBranch"] = environment.get_git_branch()
        data[pipeline_data.PACKAGE_JSON]["se.kth.gitCommit"] = environment.get_git_commit_clamped()
        data[pipeline_data.PACKAGE_JSON]["se.kth.buildDate"] = environment.get_time()

        self.write_updated_package_json(data)

        # Skip publish on pull request testing
        if environment.get_pull_request_test():
            return data
        if data[pipeline_data.NPM_VERSION_CHANGED]:
            self.log.info(
                'Package will be published. Local version is %s and '
                'latest version on npm is %s',
                data[pipeline_data.NPM_PACKAGE_VERSION],                data[pipeline_data.NPM_LATEST_VERSION]
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
