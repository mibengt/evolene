__author__ = 'tinglev'

import os
import re
from modules.pipeline_steps.abstract_pipeline_step import AbstractPipelineStep

class DockerConfPipelineStep(AbstractPipelineStep):

    def get_required_env_variables(self):
        return ['PROJECT_ROOT_PATH']

    def get_required_data_keys(self):
        return []

    def _get_docker_conf_path(self):
        return os.environ['PROJECT_ROOT_PATH'] + '/docker.conf'

    def _get_docker_conf_lines(self):
        try:
            with open(self._get_docker_conf_path()) as d_conf:
                return d_conf.read().splitlines()
        except IOError as ioe:
            self._handle_step_error('Could not read docker.conf', ioe)

    def _missing_conf_vars(self, lines):
        required = ['IMAGE_NAME', 'IMAGE_VERSION']
        variables = [line.split('=')[0] for line in lines]
        missing = [req for req in required if req not in variables]
        return missing

    def run_step(self, data):
        lines = self._get_docker_conf_lines()
        env_lines = [line for line in lines if re.match('^([a-zA-Z0-9_]+)=(.+)$', line)]
        missing_conf_vars = self._missing_conf_vars(env_lines)
        if missing_conf_vars:
            self._handle_step_error('Missing the following environment variables in docker.conf: {}'
                                    .format(missing_conf_vars))
        for env in env_lines:
            data[env.split('=')[0]] = env.split('=')[1]
        return data

