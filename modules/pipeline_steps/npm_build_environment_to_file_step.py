__author__ = 'tinglev'

import json
from modules.pipeline_steps.abstract_pipeline_step import AbstractPipelineStep
from modules.util import pipeline_data
from modules.util import environment
from modules.util import file_util

class NpmBuildEnvironmentToFileStep(AbstractPipelineStep):


    def __init__(self):
        AbstractPipelineStep.__init__(self)

    def get_required_env_variables(self):
        return [environment.GIT_BRANCH, environment.GIT_COMMIT]

    def get_required_data_keys(self):
        return []

    def run_step(self, data):
        self.write()
        return data

    def get_ouput_file(self):
        return 'build-information.js'

    def write(self):
        try:
            file_util.overwite(self.get_ouput_file(), self.get_output())
        except IOError as ioe:
            self.handle_step_error("Unable to write npm build information to file '{}'".format(
                self.get_ouput_file()))

    def get_output(self):
        return self.to_js_module()

    def to_js_module(self):
        return "module.exports = {}".format(json.dumps(self.get_build_environment()))

    def get_build_environment(self):

        return {
            "gitBranch": environment.get_git_branch(),
            "gitCommit": environment.get_git_commit(),
            "buildNumber": environment.get_build_number(),
            "buildDate": environment.get_time()
        }
