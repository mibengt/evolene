__author__ = 'tinglev'

from modules.pipeline_steps.abstract_pipeline_step import AbstractPipelineStep
from modules.util.environment import Environment
from modules.util import pipeline_data
from modules.util import file_util


class DockerFileStep(AbstractPipelineStep):

    FILE_DOCKERFILE = "/Dockerfile"

    def get_required_env_variables(self): # pragma: no cover
        return [Environment.PROJECT_ROOT]

    def get_required_data_keys(self): # pragma: no cover
        return []

    def run_step(self, data):
        if not file_util.is_file(DockerFileStep.FILE_DOCKERFILE):
            self.handle_step_error('Could not find Dockerfile at "{}"'.format(
                DockerFileStep.FILE_DOCKERFILE))

        data[pipeline_data.DOCKERFILE_FILE] = file_util.get_absolue_path(DockerFileStep.FILE_DOCKERFILE)

        return data
