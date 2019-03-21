__author__ = 'bjofra'

from modules.pipeline_steps.abstract_pipeline_step import AbstractPipelineStep
from modules.util import environment
from modules.util import pipeline_data
from modules.util import file_util


class DockerCreateBuildArgStep(AbstractPipelineStep):

    def get_required_env_variables(self): # pragma: no cover
        return [environment.PROJECT_ROOT]

    def get_required_data_keys(self): # pragma: no cover
        return []

    def run_step(self, data):
        docker_build_arg = environment.get_docker_build_arg()
        if docker_build_arg:
            data[pipeline_data.BUILD_ARG] = f"BUILD_ARG='{docker_build_arg}'"
        return data
