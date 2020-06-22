__author__ = 'tinglev'

import json 
from modules.pipeline_steps.abstract_pipeline_step import AbstractPipelineStep
from modules.util import environment
from modules.util.exceptions import PipelineException
from modules.util import nvm, pipeline_data


class NpmVersionChangedStep(AbstractPipelineStep):

    def __init__(self):
        AbstractPipelineStep.__init__(self)

    def get_required_env_variables(self):
        return [environment.PROJECT_ROOT]

    def get_required_data_keys(self):
        return [pipeline_data.NPM_PACKAGE_VERSION, pipeline_data.NPM_PACKAGE_NAME]

    def run_step(self, data):

        current_version = data[pipeline_data.NPM_PACKAGE_VERSION]
        latest = self.get_latest_version(data)
        latest_major_minor = self.get_latest_version_for_major_minor(data)

        data[pipeline_data.NPM_LATEST_VERSION] = latest
        data[pipeline_data.NPM_LATEST_MAJOR_MINOR] = latest_major_minor
        data[pipeline_data.NPM_VERSION_CHANGED] = (current_version != latest)
        t = self.is_version_already_published(data)

        self.log.debug('npm version has changed "%s"',
                       data[pipeline_data.NPM_VERSION_CHANGED])
        return data

    def is_version_already_published(self, data):
        result = True
        version = self.check_npm_for_version(data)
        if not version:
            self.log.info("Version exist '%s'", version)
            result = False
        return result
                

    def check_npm_for_version(self, data):
        '''
        Check to see if a major.minor.patch version is already published to npm registry.
        '''
        result = None
        name = data[pipeline_data.NPM_PACKAGE_NAME]
        version = data[pipeline_data.NPM_PACKAGE_VERSION]
        try:
            result = nvm.exec_npm_command(
                data, f'view {name}@"{version}" version', '-json')
        except PipelineException as npm_ex:
            self.log.info(
                "faild to read find any version for %s %s. \n %s", name, version, npm_ex)
        return result

    def get_latest_version(self, data):
        '''
        Gets the latest version for a package name from npm registry.
        '''
        name = data[pipeline_data.NPM_PACKAGE_NAME]
        try:
            # npm view @babel/core version -json
            return nvm.exec_npm_command(data, f'show {name} version')

        except PipelineException as npm_ex:
            self.log.info("Could not find any previous versions. %s", npm_ex)

        return None

    def get_versions_for_major_minor(self, data):
        '''
        Gets the latest versionws for a specific major.minor version from npm registry as an array.
        '''
        result = []
        name = data[pipeline_data.NPM_PACKAGE_NAME]
        version = self.get_major_minor(data)
        try:
            # npm view @babel/core@'7.9' version -json
            #
            # [
            #   "7.9.0",
            #   "7.9.6"
            # ]
            cli_result = nvm.exec_npm_command( data, f'view {name}@"{version}" version', '-json')
            result = json.loads(cli_result)

            self.log.info(
                "Latest published versions for %s %s is '%s'", name, version, result)

        except PipelineException as npm_ex:
            self.log.info("Error reading previous versions. %s", npm_ex)

        return result

    def get_latest_version_for_major_minor(self, data):
        '''
        Gets the latest version for a specific major.minor version from npm registry.
        '''
        try:
            versions = self.get_versions_for_major_minor(data)
            result = versions[-1] # last element
            self.log.info(
                "Latest published version is '%s'", result)
            return result

        except IndexError as e:
            self.log.info("Could not find any previous versions.")

        return None

    def get_major_minor(self, data):
        '''
        Gets the major minor didgits = "[1.2].3"
        '''
        version = data[pipeline_data.NPM_PACKAGE_VERSION]
        patch_version_index = version.rfind(".")
        result = version[:patch_version_index]
        self.log.info(
            "Major.minor specified in package.json version '%s' is '%s", version, result)

        return result
