__author__ = 'tinglev'

import json
from modules.pipeline_steps.abstract_pipeline_step import AbstractPipelineStep
from modules.util.environment import Environment
from modules.util.data import Data
from modules.util.image_version_util import ImageVersionUtil

class BuildEnvironmentToFileStep(AbstractPipelineStep):

    def get_required_env_variables(self):
        return [Environment.GIT_BRANCH, Environment.GIT_COMMIT]

    def get_required_data_keys(self):
        return [Data.IMAGE_VERSION, Data.IMAGE_NAME]

    def run_step(self, data):
        self.write(data)

    def get_local_file_path(self):
        output_file = Environment.get_build_information_output_file()
        if output_file:
            return output_file
        return '/config/version.js'

    def get_ouput_file(self):
        stripped_root = Environment.get_project_root().rstrip('/')
        return '{}{}'.format(stripped_root, self.get_local_file_path())

    def write(self, data):
        try:
            # If the output file already exists over write it.
            with open(self.get_ouput_file(), 'w+') as output_file:
                return output_file.write(self.to_js_module(self.get_file_content_as_dict(data)))

        except IOError as ioe:
            self.handle_step_error("Unable to write build information to file '{}'".format(self.get_ouput_file()), ioe)

    def to_js_module(self, file_content_as_dict):
        return "module.exports = {}".format(json.dumps(file_content_as_dict))

    def get_file_content_as_dict(self, data):

        return {
                "gitBranch": Environment.get_git_branch(),
                "gitCommit": Environment.get_git_commit(),
                "jenkinsBuild": Environment.get_build_number(),
                "jenkinsBuildDate": Environment.get_time(),
                "dockerName": data[Data.IMAGE_NAME],
                "dockerVersion": data[Data.IMAGE_VERSION],
                "image": ImageVersionUtil.prepend_registry(ImageVersionUtil.get_image(data))
        }

