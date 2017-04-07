__author__ = 'tinglev'

import os
import re
from modules.pipeline_steps.abstract_pipeline_step import AbstractPipelineStep

class DockerConfPipelineStep(AbstractPipelineStep):

    IMAGE_NAME = 'IMAGE_NAME'
    IMAGE_VERSION = 'IMAGE_VERSION'
    PROJECT_ROOT = 'PROJECT_ROOT_PATH'

    def get_required_env_variables(self):
        return [DockerConfPipelineStep.PROJECT_ROOT]

    def get_required_data_keys(self):
        return []

    def run_step(self, data):
        raw_lines = self._get_docker_conf_lines()
        env_lines = self._get_docker_conf_env_lines(raw_lines)
        missing_conf_vars = self._missing_conf_vars(env_lines)
        if missing_conf_vars:
            self._handle_step_error('Missing the following environment variables in docker.conf: {}'
                                    .format(missing_conf_vars))
        data = self._add_env_lines_to_data(env_lines, data)
        return data

    def _clean_variable_value(self, value):
        return value.replace('"', '')

    def _add_env_lines_to_data(self, env_lines, data):
        for env in env_lines:
            data[env.split('=')[0]] = self._clean_variable_value(env.split('=')[1])
        return data

    def _get_docker_conf_path(self):
        return os.environ[DockerConfPipelineStep.PROJECT_ROOT] + '/docker.conf'

    def _get_docker_conf_env_lines(self, raw_lines):
        return [line for line in raw_lines if re.match('^([a-zA-Z0-9_]+)=(.+)$', line)]

    def _get_docker_conf_lines(self):
        try:
            with open(self._get_docker_conf_path()) as d_conf:
                return d_conf.read().splitlines()
        except IOError as ioe:
            self._handle_step_error('Could not read docker.conf', ioe)

    def _missing_conf_vars(self, lines):
        required = [DockerConfPipelineStep.IMAGE_NAME, DockerConfPipelineStep.IMAGE_VERSION]
        variables = [line.split('=')[0] for line in lines]
        missing = [req for req in required if req not in variables]
        return missing
