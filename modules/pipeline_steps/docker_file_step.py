__author__ = 'tinglev'

import os
from modules.pipeline_steps.abstract_pipeline_step import AbstractPipelineStep
from modules.util.environment import Environment
from modules.util.data import Data

class DockerFileStep(AbstractPipelineStep):

    def get_required_env_variables(self):
        return [Environment.PROJECT_ROOT]

    def get_required_data_keys(self):
        return []

    def _get_docker_file_path(self):
        return '{}/Dockerfile'.format(Environment.get_project_root())

    def _docker_file_exists(self):
        return os.path.isfile(self._get_docker_file_path())

    def run_step(self, data):
        file_path = self._get_docker_file_path()
        if not self._docker_file_exists():
            self._handle_step_error('Could not find Dockerfile at "{}"'.format(file_path))
        data[Data.DOCKER_FILE] = file_path
        return data