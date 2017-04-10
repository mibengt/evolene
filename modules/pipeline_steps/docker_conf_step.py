__author__ = 'tinglev'

import re
from modules.pipeline_steps.abstract_pipeline_step import AbstractPipelineStep
from modules.util.environment import Environment
from modules.util.data import Data

class DockerConfPipelineStep(AbstractPipelineStep):

    def get_required_env_variables(self):
        return [Environment.PROJECT_ROOT]

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
        data[Data.DOCKER_CONF_FILE] = self._get_docker_conf_path()
        return data

    def _clean_variable_value(self, value):
        return value.replace('"', '')

    def _add_env_lines_to_data(self, env_lines, data):
        for env in env_lines:
            data[env.split('=')[0]] = self._clean_variable_value(env.split('=')[1])
        return data

    def _get_docker_conf_path(self):
        return Environment.get_project_root() + '/docker.conf'

    def _get_docker_conf_env_lines(self, raw_lines):
        return [line for line in raw_lines if re.match(r'^([a-zA-Z0-9_]+)=(.+)$', line)]

    def _get_docker_conf_lines(self):
        try:
            with open(self._get_docker_conf_path()) as d_conf:
                return d_conf.read().splitlines()
        except IOError as ioe:
            self._handle_step_error('Could not read docker.conf', ioe)

    def _missing_conf_vars(self, lines):
        required = [Environment.IMAGE_NAME, Environment.IMAGE_VERSION]
        variables = [line.split('=')[0] for line in lines]
        missing = [req for req in required if req not in variables]
        return missing
