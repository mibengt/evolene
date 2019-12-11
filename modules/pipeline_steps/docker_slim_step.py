__author__ = 'tinglev'

from modules.pipeline_steps.abstract_pipeline_step import AbstractPipelineStep
from modules.pipeline_steps.tag_image_step import TagImageStep
from modules.util import (
    pipeline_data,
    environment, image_version_util,
    process
)

class DockerSlimStep(AbstractPipelineStep):

    def get_required_env_variables(self):
        return []

    def get_required_data_keys(self):
        return [pipeline_data.IMAGE_NAME, pipeline_data.IMAGE_VERSION, pipeline_data.SEM_VER]

    def run_step(self, data):
        if environment.get_experimental():
            # Tag the original image names
            tag_step = TagImageStep()
            data = tag_step.run_step(data)
            self.run_docker_slim(data)
            data[pipeline_data.IMAGE_NAME] = f'{data[pipeline_data.IMAGE_NAME]}.slim'
        return data

    def run_docker_slim(self, data):
        image = image_version_util.prepend_registry(
            image_version_util.get_image(data)
        )
        self.log.debug('Running /var/lib/jenkins/docker-slim build %s', image)
        process.run_with_output(f'/var/lib/jenkins/docker-slim build {image}')
