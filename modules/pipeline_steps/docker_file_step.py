__author__ = 'tinglev'

from modules.pipeline_steps.abstract_pipeline_step import AbstractPipelineStep
from modules.util.environment import Environment
from modules.util.data import Data
from modules.util.file_util import FileUtil


class DockerFileStep(AbstractPipelineStep):

    FILE_DOCKERFILE = "/Dockerfile"

    def get_required_env_variables(self): # pragma: no cover
        return [Environment.PROJECT_ROOT]

    def get_required_data_keys(self): # pragma: no cover
        return []

    def run_step(self, data):
        if not FileUtil.is_file(DockerFileStep.FILE_DOCKERFILE):
            self.handle_step_error('Could not find Dockerfile at "{}"'.format(
                DockerFileStep.FILE_DOCKERFILE))

        data[Data.DOCKERFILE_FILE] = FileUtil.get_absolue_path(DockerFileStep.FILE_DOCKERFILE)

        return data
