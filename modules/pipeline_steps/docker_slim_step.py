__author__ = 'tinglev'

from modules.pipeline_steps.abstract_pipeline_step import AbstractPipelineStep
from modules.util import (
    pipeline_data,
    environment,
    process
)

class DockerSlimStep(AbstractPipelineStep):

    def get_required_env_variables(self):
        return []

    def get_required_data_keys(self):
        return [pipeline_data.LOCAL_IMAGE_ID]

    def run_step(self, data):
        if environment.get_experimental():
            self.run_docker_slim(data)
            data[pipeline_data.IMAGE_NAME] = f'{data[pipeline_data.IMAGE_NAME]}.slim'
        return data

    def run_docker_slim(self, data):
        image_id = data[pipeline_data.LOCAL_IMAGE_ID]
        process.run_with_output(f'docker run --rm '
                                f'-v /var/run/docker.sock:/var/run/docker.sock '
                                f'dslim/docker-slim build '
                                f'{image_id}')
