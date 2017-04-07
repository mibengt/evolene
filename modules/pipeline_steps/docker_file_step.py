__author__ = 'tinglev'

import os
from modules.pipeline_steps.abstract_pipeline_step import AbstractPipelineStep
from modules.util.environment import Environment

class DockerFileStep(AbstractPipelineStep):

    def get_required_env_variables(self):
        return [Environment.PROJECT_ROOT]

    def get_required_data_keys(self):
        return []

    def _get_docker_file_path(self):
        return '{}/Dockerfile'.format(os.environ[Environment.PROJECT_ROOT])

    def _docker_file_exists(self):
        return os.path.isfile(self._get_docker_file_path())

    def run_step(self, data):
        if not self._docker_file_exists():
            file_path = self._get_docker_file_path()
            self._handle_step_error('Could not find Dockerfile at "{}"'.format(file_path))
        return data
