__author__ = 'tinglev'

import json
from modules.pipeline_steps.abstract_pipeline_step import AbstractPipelineStep
from modules.util.environment import Environment
from modules.util.data import Data
from modules.util.image_version_util import ImageVersionUtil
from modules.util.file_util import FileUtil


class BuildEnvironmentToFileStep(AbstractPipelineStep):

    def get_required_env_variables(self):
        return [Environment.GIT_BRANCH, Environment.GIT_COMMIT]

    def get_required_data_keys(self):
        return [Data.IMAGE_VERSION, Data.IMAGE_NAME]

    def run_step(self, data):
        if Environment.get_build_information_output_file():
            self.write(data)

    def get_ouput_file(self):
        return Environment.get_build_information_output_file()

    def write(self, data):
        try:
            FileUtil.overwite(self.get_ouput_file(), self.get_output(data))

        except IOError as ioe:
            self.handle_step_error("*{}* Unable to write build information to file '{}'".format(
                ImageVersionUtil.get_image(data),
                self.get_ouput_file()))

    def get_output(self, data):
        output_file = self.get_ouput_file()
        if str(output_file).endswith(".js"):
            return self.to_js_module(data)
        if str(output_file).endswith(".json"):
            return self.to_json(data)
        if str(output_file).endswith(".ts"):
            return self.to_ts_const(data)
        if str(output_file).endswith(".conf"):
            return self.to_conf(data)

    def to_ts_const(self, data):
        return "export const buildInfo = {}".format(json.dumps(self.get_build_environment(data)))

    def to_json(self, data):
        return json.dumps(self.get_build_environment(data))

    def to_js_module(self, data):
        return "module.exports = {}".format(json.dumps(self.get_build_environment(data)))

    def to_conf(self, data):
        result = ""
        envs = self.get_build_environment(data)
        for env in envs:
            result += "{}={}\n".format(env, envs[env])
        return result

    def get_build_environment(self, data):

        return {
            "gitBranch": Environment.get_git_branch(),
            "gitCommit": Environment.get_git_commit(),
            "jenkinsBuild": Environment.get_build_number(),
            "jenkinsBuildDate": Environment.get_time(),
            "dockerName": data[Data.IMAGE_NAME],
            "dockerVersion": data[Data.IMAGE_VERSION],
            "dockerImage": ImageVersionUtil.prepend_registry(ImageVersionUtil.get_image(data))
        }
