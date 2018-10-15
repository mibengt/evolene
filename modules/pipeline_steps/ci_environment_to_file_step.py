__author__ = 'tinglev'

import re
import os
import json
from modules.pipeline_steps.abstract_pipeline_step import AbstractPipelineStep
from modules.util.environment import Environment
from modules.util.data import Data

class CiEnvironmentToFileStep(AbstractPipelineStep):

    def get_required_env_variables(self):
        return [Environment.GIT_BRANCH, Environment.GIT_COMMIT]

    def get_required_data_keys(self):
        return [Data.IMAGE_VERSION, Data.IMAGE_NAME]

    def run_step(self, data):
        self.write(data)

    def get_ouput_file(self):
        stripped_root = Environment.get_project_root().rstrip('/')
        return '{}{}'.format(stripped_root, Environment.get_build_information_output_file())

    def write(self, data):
        try:
            with open(self.get_ouput_file()) as output_file:
                return output_file.write(json.dumps(self.get_file_content_as_dict(data)))
        except IOError as ioe:
            self.handle_step_error("Unable to write ci envs to file '{}'".format(self.get_ouput_file()), ioe)

    def get_file_content_as_dict(self, data):

        return {
                "gitBranch": Environment.get_git_branch(),
                "gitCommit": Environment.get_git_commit(),
                "jenkinsBuild": Environment.get_build_number(),
                "jenkinsBuildDate": Environment.get_time(),
                "dockerName": data[Data.IMAGE_NAME],
                "dockerVersion": data[Data.IMAGE_VERSION]
        }

