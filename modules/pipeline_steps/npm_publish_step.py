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

    def should_auto_update(self, data):
        try:
            major_minor_version = data[pipeline_data.PACKAGE_JSON]["se.kth.version"]
        except:
            return False

        if major_minor_version is not None:
            if major_minor_version.count('.') != 1:
                raise ValueError('se.kth.version must be onlys major.minor')
            self.log.info('Will auto increase patch version package.json based on : %s', major_minor_version)
            return True
        self.log.info('Will not auto increase patch version in package.json')
        return False

    def get_latest_patch_version(self, data):
        version = data[pipeline_data.NPM_LATEST_VERSION]
        self.log.info('Last published version on MPM: %s', version)
        # Read the last didgit = "1.2.[3]"
        patch_version_index = version.rfind(".") + 1
        patch_version = version[patch_version_index:]
        self.log.debug('Next free patch version is: %s', patch_version)
        return int(patch_version)

    def get_auto_update_version(self, data):
        major_minor_version = data[pipeline_data.PACKAGE_JSON]["se.kth.version"]
        updated_patch_version = self.get_latest_patch_version(data) + 1
        version = f"{major_minor_version}.{updated_patch_version}"
        self.log.info('Auto update resulted in npm publish using %s as version', version)
        data[pipeline_data.NPM_PACKAGE_VERSION] = version
        return version

    def write_auto_updated_package_json(self, data):
        data[pipeline_data.PACKAGE_JSON]["version"] = self.get_auto_update_version(data)
        data[pipeline_data.PACKAGE_JSON]["se.kth.gitBranch"] = environment.get_git_branch()
        data[pipeline_data.PACKAGE_JSON]["se.kth.gitCommit"] = environment.get_git_commit()
        data[pipeline_data.PACKAGE_JSON]["se.kth.buildDate"] = environment.get_time()
        
        file_util.overwite('/package.json', json.dumps(data[pipeline_data.PACKAGE_JSON]))
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
