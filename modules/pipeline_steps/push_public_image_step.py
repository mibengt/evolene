__author__ = 'tinglev'

from requests import get, HTTPError, ConnectTimeout, RequestException
from requests.auth import HTTPBasicAuth
from modules.pipeline_steps.abstract_pipeline_step import AbstractPipelineStep
from modules.util.environment import Environment
from modules.util.data import Data
from modules.util.exceptions import PipelineException
from modules.util.docker import Docker

class PushPublicImageStep(AbstractPipelineStep):

    def run_step(self, data):
        self.push_image(data)
        return data

    def get_image_to_push(self, data):
        self.log.debug('Pushing image to public registry.')
        return '{}/{}:{}'.format(Environment.get_registry_host(),
                                 data[Data.IMAGE_NAME],
                                 data[Data.IMAGE_VERSION])

    def push_image(self, data):
        registry_image_name = self.get_image_to_push(data)
        Docker.push(registry_image_name)
        self.log.info('Pushed image "%s" to registry', registry_image_name)


    def get_required_env_variables(self):
        return [Environment.PUSH_PUBLIC]

    def get_required_data_keys(self):
        return [Data.IMAGE_NAME, Data.IMAGE_VERSION]
