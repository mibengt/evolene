__author__ = 'tinglev'

from modules.pipeline_steps.abstract_pipeline_step import AbstractPipelineStep
from modules.util.environment import Environment
from modules.util.data import Data
from modules.util.docker import Docker

class PushPublicImageStep(AbstractPipelineStep):

    def get_required_env_variables(self):
        return [Environment.PUSH_PUBLIC]

    def get_required_data_keys(self):
        return [Data.IMAGE_NAME, Data.IMAGE_VERSION, Data.SEM_VER]

    def run_step(self, data):
        self.push_image(data)
        
        self.push_image_only_semver(data)

        return data

    def get_image_to_push(self, data):
        self.log.debug('Pushing image to Docker Hub.')
        return '{}/{}:{}'.format(Environment.get_registry_host(),
                                 data[Data.IMAGE_NAME],
                                 data[Data.IMAGE_VERSION])

    def get_image_to_push_without_hash(self, data):
        self.log.debug('Public push also pushes the image with only SemVer (No commit).')
        return '{}/{}:{}'.format(Environment.get_registry_host(),
                                 data[Data.IMAGE_NAME],
                                 data[Data.SEM_VER])

    def push_image(self, data):
        registry_image_name = self.get_image_to_push(data)
        Docker.push(registry_image_name)
        self.log.info('Pushed image %s to Docker Hub.', registry_image_name)


    def push_image_only_semver(self, data):
        registry_image_name = self.get_image_to_push_without_hash(data)
        Docker.push(registry_image_name)
        self.log.info('Pushed image %s to Docker Hub', registry_image_name)
