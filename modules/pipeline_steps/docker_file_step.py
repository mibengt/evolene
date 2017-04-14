__author__ = 'tinglev'

import os
from modules.pipeline_steps.abstract_pipeline_step import AbstractPipelineStep
from modules.util.environment import Environment
from modules.util.data import Data

class DockerFileStep(AbstractPipelineStep):

    def get_required_env_variables(self): # pragma: no cover
        return [Environment.PROJECT_ROOT]

    def get_required_data_keys(self): # pragma: no cover
        return []

    def get_docker_file_path(self):
        stripped_root = Environment.get_project_root().rstrip('/')
        return '{}/Dockerfile'.format(stripped_root)

    def docker_file_exists(self):
        return os.path.isfile(self.get_docker_file_path())

    def run_step(self, data):
        file_path = self.get_docker_file_path()
        if not self.docker_file_exists():
            self.handle_step_error('Could not find Dockerfile at "{}"'.format(file_path))
        data[Data.DOCKER_FILE] = file_path
        return data
